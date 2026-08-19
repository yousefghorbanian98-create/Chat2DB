import { randomUUID } from 'node:crypto';
import { existsSync } from 'node:fs';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import { z } from 'zod';
import type Database from 'better-sqlite3';
import type { ClipperJobState, ClipInput, JobHandle, JobProgress } from '../types';
import type { DownloadService } from './DownloadService';
import type { FFmpegService, MediaAnalysis } from './FFmpegService';
import type { FaceTimeline, LocalAIService, LocalHighlight, SpeakerTimeline } from './LocalAIService';
import type { HuggingFaceService } from './HuggingFaceService';
import type { OllamaService } from './OllamaService';

interface FinalHighlight extends LocalHighlight {
  finalScore: number;
  hook: string;
  hashtags: string[];
  reason: string;
}

const responseSchema = z.object({
  clips: z.array(z.object({
    id: z.string().min(1),
    score: z.number().min(1).max(10),
    title: z.string().min(1).max(70),
    hook: z.string().max(160),
    hashtags: z.array(z.string()).min(1).max(8),
    reason: z.string().max(500)
  }))
});

function escapeSvg(value: string): string {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
}

function mediaEvidence(clip: LocalHighlight, analysis: MediaAnalysis): number {
  const scenes = analysis.scenes.filter((time) => time >= clip.start_seconds && time <= clip.end_seconds).length;
  const peaks = analysis.audioPeaks.filter((peak) => peak.time >= clip.start_seconds && peak.time <= clip.end_seconds);
  const audio = peaks.length ? Math.max(...peaks.map((peak) => peak.score)) : 0.35;
  const sceneDensity = Math.min(1, scenes / 4);
  return audio * 0.6 + sceneDensity * 0.4;
}

function snap(value: number, silences: MediaAnalysis['silences']): number {
  const points = silences.flatMap((item) => [item.start, item.end]).filter((point) => Math.abs(point - value) <= 1.5);
  return points.sort((left, right) => Math.abs(left - value) - Math.abs(right - value))[0] ?? value;
}

function defaultMetadata(clip: LocalHighlight, category: string, evidence: number): FinalHighlight {
  return {
    ...clip,
    finalScore: Math.max(1, Math.min(10, Math.round((clip.score * 0.075 + evidence * 2.5) * 10) / 10)),
    hook: clip.transcript.slice(0, 150),
    hashtags: ['#Shorts', category === 'Auto' ? '#Highlights' : `#${category.replace(/\s+/g, '')}`],
    reason: 'Selected locally from transcript quality, hook words, speech pace, audio energy, and scene changes.'
  };
}

export class ClipperEngine {
  private readonly jobs = new Map<string, ClipperJobState>();
  private readonly cancelled = new Set<string>();

  constructor(
    private readonly db: Database.Database,
    private readonly downloads: DownloadService,
    private readonly ffmpeg: FFmpegService,
    private readonly localAI: LocalAIService,
    private readonly huggingFace: HuggingFaceService,
    private readonly ollama: OllamaService,
    private readonly temp: string,
    private readonly musicPath: string | undefined,
    private readonly fontsDirectory: string,
    private readonly emit: (channel: string, value: unknown) => void
  ) {}

  start(input: ClipInput): JobHandle {
    // Explicit Node import fixes `crypto is not defined` in Electron's main
    // process (the DOM type made the accidental global reference compile).
    const jobId = randomUUID();
    const now = new Date().toISOString();
    this.jobs.set(jobId, { jobId, phase: 'queued', percent: 0, status: 'running', startedAt: now, updatedAt: now });
    void this.process(jobId, input);
    return { jobId };
  }

  renderSuggested(ids: number[]): JobHandle {
    const unique = [...new Set(ids)].filter((id) => Number.isInteger(id) && id > 0).slice(0, 30);
    if (!unique.length) throw new Error('Select at least one suggested clip');
    const jobId = randomUUID();
    const now = new Date().toISOString();
    this.jobs.set(jobId, { jobId, phase: 'render-queued', percent: 0, status: 'running', startedAt: now, updatedAt: now });
    void this.processSuggestedRender(jobId, unique);
    return { jobId };
  }

  latestJob(): ClipperJobState | null {
    return [...this.jobs.values()].sort((left, right) => right.startedAt.localeCompare(left.startedAt))[0] ?? null;
  }

  cancel(jobId: string): boolean {
    const job = this.jobs.get(jobId);
    if (!job || job.status !== 'running') return false;
    this.cancelled.add(jobId);
    this.localAI.cancel(jobId);
    this.jobs.set(jobId, { ...job, status: 'failed', phase: 'cancelled', error: 'Cancelled by user', updatedAt: new Date().toISOString() });
    return true;
  }

  private ensureActive(jobId: string): void {
    if (this.cancelled.has(jobId)) throw new Error('Cancelled by user');
  }

  private progress(jobId: string, phase: string, percent: number, message?: string): void {
    const previous = this.jobs.get(jobId);
    const monotonicPercent = Math.max(previous?.percent ?? 0, Math.min(100, Math.round(percent)));
    const value: JobProgress = { jobId, phase, percent: monotonicPercent, message };
    if (previous) this.jobs.set(jobId, { ...previous, ...value, status: 'running', updatedAt: new Date().toISOString() });
    this.emit('job:progress', value);
  }

  private async enrichWithOllama(input: ClipInput, candidates: FinalHighlight[]): Promise<FinalHighlight[]> {
    const prompt = `You are a Persian/English short-form video editor. Rank and label the supplied LOCAL candidates. Do not invent timestamps and do not change candidate ids. Category: ${input.category}. Return exactly ${String(Math.min(input.count, candidates.length))} unique clips. Return ONLY JSON {"clips":[{"id":"highlight-01","score":8.5,"title":"max 70 chars","hook":"short hook","hashtags":["#Shorts"],"reason":"why"}]}. Candidates: ${JSON.stringify(candidates.map((clip) => ({ id: clip.id, localScore: clip.finalScore, transcript: clip.transcript.slice(0, 1800) })))}`;
    let parsed: z.infer<typeof responseSchema> | undefined;
    let lastError: unknown;
    for (let attempt = 0; attempt < 3 && !parsed; attempt++) {
      try { parsed = responseSchema.parse(JSON.parse(await this.ollama.generate(input.model, prompt))); }
      catch (error: unknown) { lastError = error; }
    }
    if (!parsed) throw lastError instanceof Error ? lastError : new Error('Ollama returned invalid clip metadata');
    const byId = new Map(candidates.map((candidate) => [candidate.id, candidate]));
    const selected: FinalHighlight[] = [];
    for (const item of parsed.clips) {
      const source = byId.get(item.id);
      if (!source || selected.some((clip) => clip.id === item.id)) continue;
      selected.push({ ...source, finalScore: item.score, title: item.title, hook: item.hook, hashtags: item.hashtags, reason: item.reason });
      if (selected.length >= input.count) break;
    }
    if (!selected.length) throw new Error('Ollama did not select a valid local candidate id');
    return selected;
  }

  private async processSuggestedRender(jobId: string, ids: number[]): Promise<void> {
    try {
      const placeholders = ids.map(() => '?').join(',');
      const rows = this.db.prepare(`SELECT id,source_path,start_time,end_time,score,suggested_title,hook,hashtags,reason,caption_path,render_options_json FROM clips WHERE id IN (${placeholders}) AND status IN ('suggested','approved')`).all(...ids) as Array<{id:number;source_path:string;start_time:number;end_time:number;score:number;suggested_title:string;hook:string;hashtags:string;reason:string;caption_path?:string;render_options_json:string}>;
      if (!rows.length) throw new Error('The selected suggestions are no longer available');
      const directory = path.join(this.temp, jobId);
      await mkdir(directory, { recursive: true });
      const encoder = await this.ffmpeg.preferredEncoder();
      for (const [index, row] of rows.entries()) {
        this.ensureActive(jobId);
        const options = JSON.parse(row.render_options_json) as ClipInput;
        let faces: FaceTimeline | undefined;
        if (options.processingProfile === 'professional') faces = await this.localAI.trackFaces(row.source_path, { samplesPerSecond: 4, jobId });
        this.progress(jobId, 'rendering-approved', 5 + Math.round(index / rows.length * 90), `Rendering approved clip ${String(index + 1)} of ${String(rows.length)}`);
        const video = path.join(directory, `approved_clip_${String(row.id)}.mp4`);
        const rawThumb = path.join(directory, `thumb_raw_${String(row.id)}.jpg`);
        const thumb = path.join(directory, `thumb_${String(row.id)}.jpg`);
        await this.ffmpeg.render(row.source_path, row.start_time, row.end_time, video, {
          aspect: options.aspect, captionsPath: options.captions ? row.caption_path : undefined, fontsDirectory: this.fontsDirectory,
          smartZoom: options.smartZoom, blurBackground: options.blurBackground,
          musicPath: options.music && this.musicPath && existsSync(this.musicPath) ? this.musicPath : undefined,
          musicVolume: 0.12, encoder, sourceStart: row.start_time, faceSamples: faces?.samples
        });
        await this.ffmpeg.frame(row.source_path, row.start_time + Math.min(3, (row.end_time-row.start_time)/3), rawThumb);
        const overlay = Buffer.from(`<svg width="1080" height="1920"><rect y="1380" width="1080" height="540" fill="#080612" fill-opacity=".72"/><foreignObject x="70" y="1450" width="940" height="340"><div xmlns="http://www.w3.org/1999/xhtml" style="font:700 68px Arial;color:white;text-align:center">${escapeSvg(row.suggested_title)}</div></foreignObject></svg>`);
        await sharp(rawThumb).resize(1080,1920,{fit:'cover'}).composite([{input:overlay}]).jpeg({quality:90}).toFile(thumb);
        this.db.prepare("UPDATE clips SET local_path=?,thumbnail_path=?,status='pending' WHERE id=?").run(video,thumb,row.id);
        this.emit('clip:ready',{id:row.id,localPath:video,thumbnailPath:thumb});
      }
      this.progress(jobId,'done',100,`${String(rows.length)} approved clips rendered`);
      const complete=this.jobs.get(jobId);if(complete)this.jobs.set(jobId,{...complete,status:'completed',updatedAt:new Date().toISOString()});
      this.emit('job:done',{jobId});
    } catch(error:unknown) {
      const message=error instanceof Error?error.message:String(error);const failed=this.jobs.get(jobId);if(failed)this.jobs.set(jobId,{...failed,status:'failed',error:message,updatedAt:new Date().toISOString()});this.emit('job:done',{jobId,error:message});
    }
  }

  private async process(jobId: string, input: ClipInput): Promise<void> {
    try {
      const directory = path.join(this.temp, jobId);
      await mkdir(directory, { recursive: true });
      this.progress(jobId, 'source', 2, 'Preparing source video');
      let source = input.localPath;
      if (!source && input.url) {
        source = await this.downloads.download(input.url, directory, 'bestvideo[height<=1080]+bestaudio/best',
          (percent) => this.progress(jobId, 'download', Math.max(2, Math.round(percent * 0.16))));
      }
      if (!source) throw new Error('Choose a URL or local video');

      const probe = await this.ffmpeg.probe(source);
      this.progress(jobId, 'local-ai', 18, 'Starting Faster-Whisper');
      // Do not run FFmpeg's two full media-analysis passes beside CPU Whisper.
      // Competing decoders made transcription dramatically slower on laptops.
      const localCandidates = await this.localAI.analyze(source, path.join(directory, 'analysis'), {
        model: input.whisperModel,
        language: input.language,
        targetDuration: input.maxLength,
        clipCount: Math.min(30, Math.max(input.count * 3, input.count)),
        jobId
      }, (event) => {
        const stageBase: Record<string, number> = { model: 18, transcription: 26 };
        const base = stageBase[event.stage ?? ''] ?? 18;
        const span = event.stage === 'transcription' ? 22 : 7;
        const percent = typeof event.percent === 'number' ? event.percent : 0;
        this.progress(jobId, event.stage ?? 'local-ai', base + Math.round(percent * span / 100), event.detail);
      });
      this.ensureActive(jobId);
      this.progress(jobId, 'media-analysis', 49, 'Analyzing scenes, silence, and audio energy');
      const analysis = await this.ffmpeg.analyze(source);
      this.progress(jobId, 'media-analysis', 55, 'Media analysis complete');

      let speakerTimeline: SpeakerTimeline | undefined;
      let faceTimeline: FaceTimeline | undefined;
      if (input.processingProfile === 'professional') {
        const token = await this.huggingFace.accessToken();
        if (!token) throw new Error('Configure professional speaker-model access in Settings before using Professional mode');
        this.progress(jobId, 'speaker-diarization', 56, 'Identifying active speakers');
        speakerTimeline = await this.localAI.diarize(source, path.join(directory, 'speakers'), token, { minSpeakers: 1, maxSpeakers: 4, jobId }, (event) => {
          const percent = typeof event.percent === 'number' ? event.percent : 0;
          this.progress(jobId, event.stage ?? 'speaker-diarization', 56 + Math.round(percent * 0.08), event.detail);
        });
        await writeFile(path.join(directory, 'speaker-timeline.json'), JSON.stringify(speakerTimeline, null, 2), 'utf8');
        this.emit('speaker:timeline', { jobId, ...speakerTimeline });
        this.progress(jobId, 'speaker-diarization', 64, `${String(speakerTimeline.speakers.length)} speakers identified`);
        this.progress(jobId, 'face-tracking', 65, 'Creating stable face identities');
        faceTimeline = await this.localAI.trackFaces(source, { samplesPerSecond: 4, jobId }, (event) => {
          const percent = typeof event.percent === 'number' ? event.percent : 0;
          this.progress(jobId, event.stage ?? 'face-tracking', 65 + Math.round(percent * 0.09), event.detail);
        });
        await writeFile(path.join(directory, 'face-timeline.json'), JSON.stringify(faceTimeline, null, 2), 'utf8');
        this.emit('face:timeline', { jobId, ...faceTimeline });
        this.progress(jobId, 'face-tracking', 74, `${String(faceTimeline.trackCount)} face tracks created`);
      }

      let selected = localCandidates
        .map((clip) => defaultMetadata(clip, input.category, mediaEvidence(clip, analysis)))
        .sort((left, right) => right.finalScore - left.finalScore)
        .slice(0, Math.max(input.count, 1));

      if (input.analysisMode !== 'local') {
        const status = await this.ollama.status();
        if (status.running && status.models.includes(input.model)) {
          this.progress(jobId, 'ollama', input.processingProfile === 'professional' ? 75 : 56, 'Refining local candidates with Ollama');
          try { selected = await this.enrichWithOllama(input, localCandidates.map((clip) => defaultMetadata(clip, input.category, mediaEvidence(clip, analysis)))); }
          catch (error: unknown) {
            if (input.analysisMode === 'ollama') throw error;
            this.progress(jobId, 'ollama-fallback', input.processingProfile === 'professional' ? 80 : 60, `Ollama unavailable; using local ranking: ${error instanceof Error ? error.message : String(error)}`);
          }
        } else if (input.analysisMode === 'ollama') {
          throw new Error('The selected Ollama model is not running or installed');
        }
      }

      if (input.previewOnly) {
        this.db.prepare("DELETE FROM clips WHERE source_path=? AND status='suggested'").run(source);
        const insert = this.db.prepare("INSERT INTO clips(source_path,start_time,end_time,score,suggested_title,hook,hashtags,reason,caption_path,transcript,render_options_json,status) VALUES(?,?,?,?,?,?,?,?,?,?,?,'suggested')");
        const rows = this.db.transaction(() => selected.slice(0, input.count).map((suggested) => {
          const start = Math.max(0, snap(suggested.start_seconds, analysis.silences));
          const end = Math.min(probe.duration, start + input.maxLength, snap(suggested.end_seconds, analysis.silences));
          const result = insert.run(source, start, end, Math.round(suggested.finalScore), suggested.title, suggested.hook, JSON.stringify(suggested.hashtags), suggested.reason, suggested.caption_path, suggested.transcript, JSON.stringify({ ...input, localPath: source, url: undefined, previewOnly: false }));
          return { ...suggested, id: Number(result.lastInsertRowid), start, end };
        }))();
        for (const row of rows) this.emit('clip:ready', row);
        this.progress(jobId, 'preview-ready', 100, `${String(rows.length)} suggestions ready for review`);
        const completed = this.jobs.get(jobId);
        if (completed) this.jobs.set(jobId, { ...completed, status: 'completed', updatedAt: new Date().toISOString() });
        this.emit('job:done', { jobId, preview: true });
        return;
      }

      const encoder = await this.ffmpeg.preferredEncoder();
      const renderBase = input.processingProfile === 'professional' ? 82 : 62;
      const renderSpan = input.processingProfile === 'professional' ? 16 : 36;
      this.progress(jobId, 'rendering', renderBase, encoder === 'h264_nvenc' ? 'NVIDIA NVENC enabled' : 'CPU encoder enabled');
      for (const [index, suggested] of selected.slice(0, input.count).entries()) {
        this.ensureActive(jobId);
        const start = Math.max(0, snap(suggested.start_seconds, analysis.silences));
        const end = Math.min(probe.duration, start + input.maxLength, snap(suggested.end_seconds, analysis.silences));
        if (end <= start + 1) continue;
        this.progress(jobId, 'rendering', renderBase + Math.round(index / selected.length * renderSpan), `Rendering clip ${String(index + 1)}`);
        const video = path.join(directory, `final_clip_${String(index + 1)}.mp4`);
        const rawThumb = path.join(directory, `thumb_raw_${String(index + 1)}.jpg`);
        const thumb = path.join(directory, `thumb_${String(index + 1)}.jpg`);
        await this.ffmpeg.render(source, start, end, video, {
          aspect: input.aspect,
          captionsPath: input.captions ? suggested.caption_path : undefined,
          fontsDirectory: this.fontsDirectory,
          smartZoom: input.smartZoom,
          blurBackground: input.blurBackground,
          musicPath: input.music && this.musicPath && existsSync(this.musicPath) ? this.musicPath : undefined,
          musicVolume: 0.12,
          encoder,
          sourceStart: start,
          faceSamples: faceTimeline?.samples
        });
        const scene = analysis.scenes.filter((time) => time >= start && time <= end)
          .sort((left, right) => Math.abs(left - (start + (end - start) * 0.3)) - Math.abs(right - (start + (end - start) * 0.3)))[0];
        await this.ffmpeg.frame(source, scene ?? start + (end - start) * 0.3, rawThumb);
        const overlay = Buffer.from(`<svg width="1080" height="1920"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="55%" stop-color="black" stop-opacity="0"/><stop offset="100%" stop-color="black" stop-opacity="0.9"/></linearGradient></defs><rect width="1080" height="1920" fill="url(#g)"/><rect x="42" y="42" width="210" height="64" rx="18" fill="#ff0000"/><text x="147" y="85" text-anchor="middle" fill="white" font-family="Arial" font-size="30" font-weight="bold">SHORTS</text><foreignObject x="70" y="1420" width="940" height="390"><div xmlns="http://www.w3.org/1999/xhtml" style="font:700 68px Arial;color:white;text-align:center;text-shadow:0 4px 8px black;line-height:1.12">${escapeSvg(suggested.title)}</div></foreignObject></svg>`);
        await sharp(rawThumb).resize(1080, 1920, { fit: 'cover' }).composite([{ input: overlay }]).jpeg({ quality: 90 }).toFile(thumb);
        const row = this.db.prepare('INSERT INTO clips(source_path,start_time,end_time,score,suggested_title,hook,hashtags,reason,local_path,thumbnail_path) VALUES(?,?,?,?,?,?,?,?,?,?)')
          .run(source, start, end, Math.round(suggested.finalScore), suggested.title, suggested.hook, JSON.stringify(suggested.hashtags), suggested.reason, video, thumb);
        this.emit('clip:ready', { ...suggested, databaseId: Number(row.lastInsertRowid), start, end, localPath: video, thumbnailPath: thumb });
      }
      this.progress(jobId, 'done', 100, `${String(selected.length)} clips created`);
      const completed = this.jobs.get(jobId);
      if (completed) this.jobs.set(jobId, { ...completed, status: 'completed', updatedAt: new Date().toISOString() });
      this.emit('job:done', { jobId });
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : String(error);
      const failed = this.jobs.get(jobId);
      if (failed) this.jobs.set(jobId, { ...failed, status: 'failed', error: message, updatedAt: new Date().toISOString() });
      this.emit('job:done', { jobId, error: message });
    }
  }

  list(): unknown[] { return this.db.prepare('SELECT * FROM clips ORDER BY created_at DESC').all(); }
  get(id: number): { id: number; suggested_title: string; hashtags: string; local_path: string; thumbnail_path: string; status: string } | undefined {
    return this.db.prepare('SELECT id,suggested_title,hashtags,local_path,thumbnail_path,status FROM clips WHERE id=?').get(id) as { id: number; suggested_title: string; hashtags: string; local_path: string; thumbnail_path: string; status: string } | undefined;
  }
  update(id: number, patch: { status?: string; suggested_title?: string; hashtags?: string }): void {
    const fields = Object.entries(patch);
    if (fields.length) this.db.prepare(`UPDATE clips SET ${fields.map(([key]) => `${key}=?`).join(',')} WHERE id=?`).run(...fields.map(([, value]) => value), id);
  }
}
