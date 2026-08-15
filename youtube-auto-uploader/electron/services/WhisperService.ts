import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { readFile, rm } from 'node:fs/promises';
import path from 'node:path';

export interface WhisperOptions { executablePath?: string; modelPath?: string }
export interface TranscriptCue { start: number; end: number; text: string }

function timestamp(value: string): number {
  const parts = value.replace(',', '.').split(':').map(Number);
  if (parts.length === 3) return (parts[0] ?? 0) * 3600 + (parts[1] ?? 0) * 60 + (parts[2] ?? 0);
  return (parts[0] ?? 0) * 60 + (parts[1] ?? 0);
}

/**
 * Local speech-to-text fallback backed by a user-provided whisper.cpp CLI
 * (`whisper-cli.exe` / `main.exe`) and GGML/GGUF model. Nothing is bundled, so the
 * installer stays small and no network access is ever required at runtime.
 */
export class WhisperService {
  constructor(private readonly options: () => WhisperOptions) {}

  available(): boolean {
    const { executablePath, modelPath } = this.options();
    return Boolean(executablePath && modelPath && existsSync(executablePath) && existsSync(modelPath));
  }

  /** Transcribes an audio/video file and returns caption cues, or [] when whisper is not configured. */
  async transcribe(mediaFile: string, workingDirectory: string, signal?: AbortSignal): Promise<TranscriptCue[]> {
    if (!this.available()) return [];
    const { executablePath, modelPath } = this.options();
    const outputBase = path.join(workingDirectory, 'whisper-transcript');
    await new Promise<void>((resolve, reject) => {
      if (signal?.aborted) { reject(new Error('Cancelled')); return; }
      const child = spawn(executablePath as string, ['-m', modelPath as string, '-f', mediaFile, '-osrt', '-of', outputBase, '-np'], { windowsHide: true });
      const onAbort = (): void => { child.kill('SIGKILL'); };
      signal?.addEventListener('abort', onAbort, { once: true });
      let stderr = '';
      child.stderr.setEncoding('utf8');
      child.stderr.on('data', (chunk: string) => { stderr += chunk; });
      child.once('error', (error) => { signal?.removeEventListener('abort', onAbort); reject(error); });
      child.once('close', (code) => {
        signal?.removeEventListener('abort', onAbort);
        if (signal?.aborted) { reject(new Error('Cancelled')); return; }
        if (code === 0) resolve(); else reject(new Error(stderr || `whisper exited ${String(code)}`));
      });
    });
    const srtFile = `${outputBase}.srt`;
    if (!existsSync(srtFile)) return [];
    const cues = parseSrt(await readFile(srtFile, 'utf8'));
    await rm(srtFile, { force: true });
    return cues;
  }
}

export function parseSrt(value: string): TranscriptCue[] {
  const blocks = value.replaceAll('\r', '').split(/\n\n+/);
  const cues: TranscriptCue[] = [];
  for (const block of blocks) {
    const lines = block.split('\n').filter(Boolean);
    const timingIndex = lines.findIndex((line) => line.includes('-->'));
    if (timingIndex < 0) continue;
    const match = /([\d:,.]+)\s+-->\s+([\d:,.]+)/.exec(lines[timingIndex] ?? '');
    if (!match?.[1] || !match[2]) continue;
    const text = lines.slice(timingIndex + 1).join(' ').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    if (text) cues.push({ start: timestamp(match[1]), end: timestamp(match[2]), text });
  }
  return cues;
}
