import { EventEmitter } from 'node:events';
import { mkdir, rm } from 'node:fs/promises';
import path from 'node:path';
import type Database from 'better-sqlite3';
import type { DownloadService } from './DownloadService';
import type { YouTubeService } from './YouTubeService';
import type { JobHandle, JobProgress, UploadInput } from '../types';
import { isRetryable, retry } from '../utils/retry';

interface QueuedJob {
  id: string;
  input: UploadInput;
  priority: number;
  dbId: number;
  type: 'single' | 'batch' | 'auto_sync' | 'clipper';
  controller: AbortController;
  sessionUri?: string;
}

interface StoredJob {
  id: number;
  source_url: string | null;
  source_title: string | null;
  privacy: 'public' | 'unlisted' | 'private';
  upload_type: QueuedJob['type'];
  payload_json: string | null;
  upload_session_uri: string | null;
  downloaded_path: string | null;
}

export interface QueueConcurrency { download: number; upload: number }

/**
 * Two-stage queue with separate download and upload worker pools. Each pool has its own
 * configurable concurrency. Cancellation aborts the running child process / network request.
 * All state is persisted in SQLite; interrupted jobs (including partially-uploaded resumable
 * sessions) are restored on construction.
 */
export class UploadQueue extends EventEmitter {
  private readonly downloadJobs: QueuedJob[] = [];
  private readonly uploadJobs: QueuedJob[] = [];
  private readonly running = new Map<string, QueuedJob>();
  private activeDownloads = 0;
  private activeUploads = 0;
  private paused = false;
  private closed = false;

  constructor(
    readonly db: Database.Database,
    private readonly downloads: DownloadService,
    private readonly youtube: YouTubeService,
    private readonly temp: string,
    private readonly keepDownloads: () => boolean,
    private readonly concurrency: () => QueueConcurrency = () => ({ download: 2, upload: 1 })
  ) {
    super();
    this.db.prepare("UPDATE synced_videos SET status='queued', updated_at=datetime('now') WHERE status IN ('downloading','uploading')").run();
    const interrupted = this.db.prepare("SELECT id,source_url,source_title,privacy,upload_type,payload_json,upload_session_uri,downloaded_path FROM synced_videos WHERE status='queued' ORDER BY created_at").all() as StoredJob[];
    for (const stored of interrupted) { try { this.restore(stored); } catch { /* Unrestorable rows keep their queued state for manual retry. */ } }
    queueMicrotask(() => { this.pumpAll(); });
  }

  enqueue(input: UploadInput, type: QueuedJob['type'] = 'single', channelId: number | null = null): JobHandle {
    if (!input.url && !input.localPath) throw new Error('A source URL or local file is required');
    const id = crypto.randomUUID();
    const sourceId = input.localPath ? `local:${id}` : id;
    const result = this.db.prepare("INSERT INTO synced_videos(channel_id,source_video_id,source_url,source_title,upload_type,privacy,status,payload_json) VALUES(?,?,?,?,?,?,'queued',?)")
      .run(channelId, sourceId, input.url ?? null, input.sourceTitle ?? null, type, input.privacy ?? 'unlisted', JSON.stringify(input));
    this.push({ id, input, priority: this.priority(type), dbId: Number(result.lastInsertRowid), type, controller: new AbortController() });
    return { jobId: id };
  }

  approve(databaseId: number): JobHandle {
    const stored = this.db.prepare("SELECT id,source_url,source_title,privacy,upload_type,payload_json,upload_session_uri,downloaded_path FROM synced_videos WHERE id=? AND status='pending'").get(databaseId) as StoredJob | undefined;
    if (!stored) throw new Error('Pending upload not found');
    this.db.prepare("UPDATE synced_videos SET status='queued',updated_at=datetime('now') WHERE id=?").run(databaseId);
    return this.restore(stored);
  }

  reject(databaseId: number): void {
    this.db.prepare("UPDATE synced_videos SET status='skipped',updated_at=datetime('now') WHERE id=? AND status='pending'").run(databaseId);
  }

  retryJob(databaseId: number): JobHandle {
    const stored = this.db.prepare("SELECT id,source_url,source_title,privacy,upload_type,payload_json,upload_session_uri,downloaded_path FROM synced_videos WHERE id=? AND status IN ('failed','cancelled')").get(databaseId) as StoredJob | undefined;
    if (!stored) throw new Error('Failed upload not found');
    this.db.prepare("UPDATE synced_videos SET status='queued',error_message=NULL,updated_at=datetime('now') WHERE id=?").run(databaseId);
    return this.restore(stored);
  }

  pause(): void { this.paused = true; }
  resume(): void { this.paused = false; this.pumpAll(); }

  /** Cancels a queued or actively running job. Running work is aborted, which kills yt-dlp / the upload request. */
  cancel(jobId: string): void {
    const queued = [...this.downloadJobs, ...this.uploadJobs].find((item) => item.id === jobId);
    queued?.controller.abort();
    this.running.get(jobId)?.controller.abort();
  }

  /** Aborts all active work so the process can exit without orphaned children. */
  shutdown(): void {
    this.closed = true;
    for (const job of [...this.downloadJobs, ...this.uploadJobs, ...this.running.values()]) job.controller.abort();
    this.downloadJobs.length = 0;
    this.uploadJobs.length = 0;
  }

  private restore(stored: StoredJob): JobHandle {
    let input: UploadInput;
    try {
      input = stored.payload_json ? JSON.parse(stored.payload_json) as UploadInput : {
        url: stored.source_url ?? undefined,
        sourceTitle: stored.source_title ?? undefined,
        privacy: stored.privacy
      };
    } catch {
      input = { url: stored.source_url ?? undefined, sourceTitle: stored.source_title ?? undefined, privacy: stored.privacy };
    }
    if (stored.downloaded_path && !input.localPath) input = { ...input, localPath: stored.downloaded_path };
    if (!input.url && !input.localPath) throw new Error(`Stored job ${String(stored.id)} has no source`);
    const handle = { jobId: crypto.randomUUID() };
    this.push({
      id: handle.jobId, input, priority: this.priority(stored.upload_type), dbId: stored.id,
      type: stored.upload_type, controller: new AbortController(), sessionUri: stored.upload_session_uri ?? undefined
    });
    return handle;
  }

  private push(job: QueuedJob): void {
    const target = job.input.localPath ? this.uploadJobs : this.downloadJobs;
    target.push(job);
    target.sort((left, right) => left.priority - right.priority);
    this.pumpAll();
  }

  private priority(type: QueuedJob['type']): number {
    return type === 'single' || type === 'clipper' ? 0 : type === 'batch' ? 1 : 2;
  }

  private progress(value: JobProgress): void { this.emit('progress', value); }

  private pumpAll(): void {
    if (this.closed || this.paused) return;
    const limits = this.concurrency();
    while (this.activeDownloads < Math.max(1, limits.download) && this.downloadJobs.length) {
      const job = this.downloadJobs.shift();
      if (!job) break;
      this.activeDownloads++;
      void this.runDownload(job).finally(() => { this.activeDownloads--; this.pumpAll(); });
    }
    while (this.activeUploads < Math.max(1, limits.upload) && this.uploadJobs.length) {
      const job = this.uploadJobs.shift();
      if (!job) break;
      this.activeUploads++;
      void this.runUpload(job).finally(() => { this.activeUploads--; this.pumpAll(); });
    }
  }

  private fail(job: QueuedJob, error: unknown): void {
    const message = error instanceof Error ? error.message : String(error);
    const status = job.controller.signal.aborted || message === 'Cancelled' ? 'cancelled' : 'failed';
    this.db.prepare("UPDATE synced_videos SET status=?,error_message=?,attempts=attempts+1,updated_at=datetime('now') WHERE id=?")
      .run(status, message, job.dbId);
    if (/quotaExceeded/i.test(message)) this.paused = true;
    this.emit('done', { jobId: job.id, error: message });
  }

  private async runDownload(job: QueuedJob): Promise<void> {
    const directory = path.join(this.temp, job.id);
    this.running.set(job.id, job);
    try {
      await mkdir(directory, { recursive: true });
      if (!job.input.url) throw new Error('Source URL is missing');
      this.db.prepare("UPDATE synced_videos SET status='downloading',updated_at=datetime('now') WHERE id=?").run(job.dbId);
      const metadata = await retry(() => this.downloads.metadata(job.input.url as string, job.controller.signal), { attempts: 3, retryable: isRetryable });
      this.db.prepare('UPDATE synced_videos SET source_video_id=?,source_title=?,source_channel_name=? WHERE id=?')
        .run(metadata.id, metadata.title, metadata.channel, job.dbId);
      const file = await retry(() => this.downloads.download(
        job.input.url as string,
        directory,
        job.input.quality ?? 'bestvideo[height<=1080]+bestaudio/best',
        (percent, line) => this.progress({ jobId: job.id, phase: 'downloading', percent, message: line.trim() }),
        job.controller.signal
      ), { attempts: 3, retryable: isRetryable });
      this.db.prepare("UPDATE synced_videos SET status='queued',downloaded_path=?,updated_at=datetime('now') WHERE id=?").run(file, job.dbId);
      job.input = { ...job.input, localPath: file, sourceTitle: job.input.sourceTitle ?? metadata.title, description: job.input.description ?? metadata.description };
      this.running.delete(job.id);
      this.push({ ...job, controller: new AbortController() });
    } catch (error: unknown) {
      this.running.delete(job.id);
      if (!this.keepDownloads()) await rm(directory, { recursive: true, force: true });
      this.fail(job, error);
    }
  }

  private async runUpload(job: QueuedJob): Promise<void> {
    const file = job.input.localPath;
    this.running.set(job.id, job);
    try {
      if (!file) throw new Error('Local file is missing');
      this.db.prepare("UPDATE synced_videos SET status='uploading',downloaded_path=?,updated_at=datetime('now') WHERE id=?").run(file, job.dbId);
      const sourceTitle = job.input.sourceTitle ?? job.input.title ?? 'Uploaded video';
      const title = (job.input.title ?? sourceTitle).replace('{original_title}', sourceTitle);
      const result = await retry(() => this.youtube.upload(
        file,
        { ...job.input, title, description: job.input.description ?? '' },
        {
          onProgress: (percent) => { this.progress({ jobId: job.id, phase: 'uploading', percent }); },
          onCheckpoint: (state) => {
            job.sessionUri = state.sessionUri;
            this.db.prepare('UPDATE synced_videos SET upload_session_uri=?,upload_offset=? WHERE id=?').run(state.sessionUri, state.offset, job.dbId);
          },
          signal: job.controller.signal
        },
        { sessionUri: job.sessionUri }
      ), { attempts: 3, retryable: isRetryable });
      this.db.prepare("UPDATE synced_videos SET status='success',uploaded_video_id=?,uploaded_url=?,upload_session_uri=NULL,upload_offset=0,updated_at=datetime('now') WHERE id=?")
        .run(result.id, result.url, job.dbId);
      this.db.prepare("INSERT INTO upload_history(source_url,source_title,uploaded_id,uploaded_url,upload_type,status) VALUES(?,?,?,?,?,'success')")
        .run(job.input.url ?? null, sourceTitle, result.id, result.url, job.type);
      if (job.input.clipId) this.db.prepare("UPDATE clips SET status='uploaded',uploaded_video_id=?,uploaded_url=? WHERE id=?").run(result.id, result.url, job.input.clipId);
      this.emit('done', { jobId: job.id, ...result });
      if (job.input.url && !this.keepDownloads()) await rm(path.dirname(file), { recursive: true, force: true });
    } catch (error: unknown) {
      this.fail(job, error);
    } finally {
      this.running.delete(job.id);
    }
  }

  list(status?: string): unknown[] {
    return status
      ? this.db.prepare('SELECT * FROM synced_videos WHERE status=? ORDER BY created_at DESC').all(status)
      : this.db.prepare('SELECT * FROM synced_videos ORDER BY created_at DESC').all();
  }
}
