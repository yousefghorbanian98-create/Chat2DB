import { createHash } from 'node:crypto';
import type { ChannelsRepository } from '../db/repositories/channels.repo';
import type { DownloadService } from './DownloadService';
import type { UploadQueue } from './UploadQueue';
import { cronDue, isValidCron } from '../utils/cron';

interface MonitoredChannel {
  id: number;
  youtube_channel_id: string;
  interval_hours: number;
  auto_upload: number;
  privacy: 'public' | 'unlisted' | 'private';
  is_active: number;
  last_checked_at: string | null;
  last_error: string | null;
  custom_cron: string | null;
  etag: string | null;
  next_retry_at: string | null;
  consecutive_failures: number;
}

const MAX_BACKOFF_MINUTES = 6 * 60;

/**
 * Periodic channel watcher. Every minute it evaluates which channels are due, honouring
 * per-channel hour intervals or a custom five-field cron expression. A response fingerprint
 * (etag) is stored so unchanged listings are skipped cheaply, and failures back off
 * exponentially per channel with the retry time persisted across restarts.
 */
export class ChannelMonitor {
  private timer?: NodeJS.Timeout;

  constructor(
    private readonly channels: ChannelsRepository,
    private readonly downloads: DownloadService,
    private readonly queue: UploadQueue,
    private readonly notify: (message: string) => void
  ) {}

  start(): void {
    if (this.timer) return;
    this.timer = setInterval(() => { void this.tick(); }, 60_000);
    void this.tick();
  }

  stop(): void {
    if (this.timer) clearInterval(this.timer);
    this.timer = undefined;
  }

  private due(channel: MonitoredChannel): boolean {
    if (channel.next_retry_at && Date.parse(channel.next_retry_at) > Date.now()) return false;
    if (channel.custom_cron && isValidCron(channel.custom_cron)) {
      const since = channel.last_checked_at ? Date.parse(channel.last_checked_at) : Date.now() - 24 * 60 * 60 * 1000;
      return cronDue(channel.custom_cron, Number.isFinite(since) ? since : 0);
    }
    if (!channel.last_checked_at) return true;
    const checked = Date.parse(channel.last_checked_at);
    return !Number.isFinite(checked) || Date.now() - checked >= channel.interval_hours * 3_600_000;
  }

  async tick(channelId?: number): Promise<void> {
    const rows = this.channels.list() as unknown as MonitoredChannel[];
    for (const channel of rows.filter((item) => item.is_active && (channelId === undefined ? this.due(item) : item.id === channelId))) {
      try {
        const videos = (await this.downloads.playlist(`https://www.youtube.com/channel/${channel.youtube_channel_id}/videos`)).slice(0, 20);
        const etag = createHash('sha256').update(JSON.stringify(videos.map((video) => video.id))).digest('hex');
        const now = new Date().toISOString();
        if (channel.etag === etag) {
          this.channels.update(channel.id, { last_checked_at: now, last_error: null, next_retry_at: null, consecutive_failures: 0 });
          continue;
        }
        if (!channel.last_checked_at) {
          for (const video of videos) this.markSeen(channel.id, video.id, video.title, video.url);
        } else {
          for (const video of [...videos].reverse()) {
            if (this.exists(channel.id, video.id)) continue;
            this.notify(`New video found: ${video.title}`);
            if (channel.auto_upload) this.queue.enqueue({ url: video.url, sourceTitle: video.title, title: '{original_title}', privacy: channel.privacy, quality: 'best' }, 'auto_sync', channel.id);
            else this.markSeen(channel.id, video.id, video.title, video.url, 'pending');
          }
        }
        this.channels.update(channel.id, { last_checked_at: now, last_error: null, etag, next_retry_at: null, consecutive_failures: 0 });
      } catch (error: unknown) {
        const failures = channel.consecutive_failures + 1;
        const backoffMinutes = Math.min(MAX_BACKOFF_MINUTES, 2 ** Math.min(failures, 10));
        this.channels.update(channel.id, {
          last_checked_at: new Date().toISOString(),
          last_error: error instanceof Error ? error.message : String(error),
          consecutive_failures: failures,
          next_retry_at: new Date(Date.now() + backoffMinutes * 60_000).toISOString()
        });
      }
    }
  }

  private exists(channelId: number, videoId: string): boolean {
    return Boolean(this.queue.db.prepare('SELECT 1 FROM synced_videos WHERE channel_id=? AND source_video_id=?').get(channelId, videoId));
  }

  private markSeen(channelId: number, id: string, title: string, url: string, status = 'skipped'): void {
    this.queue.db.prepare('INSERT OR IGNORE INTO synced_videos(channel_id,source_video_id,source_title,source_url,upload_type,status) VALUES(?,?,?,?,?,?)')
      .run(channelId, id, title, url, 'auto_sync', status);
  }
}
