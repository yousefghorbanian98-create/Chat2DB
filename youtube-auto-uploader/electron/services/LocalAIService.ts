import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { app } from 'electron';

export interface LocalHighlight {
  id: string;
  start_seconds: number;
  end_seconds: number;
  score: number;
  title: string;
  transcript: string;
  caption_path: string;
}

export interface LocalEngineStatus {
  available: boolean;
  engineVersion?: string;
  cudaAvailable: boolean;
  recommendedModels: string[];
  error?: string;
}

export interface LocalModelInfo { name: string; installed: boolean; sizeBytes: number }
export interface SpeakerTurn { speaker: string; start_seconds: number; end_seconds: number }
export interface SpeakerTimeline { speakers: string[]; turns: SpeakerTurn[] }

interface EngineResult {
  ok: boolean;
  error?: string;
  highlights?: LocalHighlight[];
  engineVersion?: string;
  cudaAvailable?: boolean;
  recommendedModels?: string[];
  models?: LocalModelInfo[];
  speakers?: string[];
  turns?: SpeakerTurn[];
}

interface EngineProgress {
  event?: string;
  stage?: string;
  percent?: number | null;
  detail?: string;
  message?: string;
}

const allowedModels = new Set(['tiny', 'base', 'small', 'medium', 'large-v3']);

export class LocalAIService {
  private readonly binaryDirectory: string;
  private readonly script: string;
  private readonly cacheDirectory: string;
  private readonly children = new Map<string, ReturnType<typeof spawn>>();

  constructor() {
    this.cacheDirectory = path.join(app.getPath('userData'), 'cache', 'local-ai');
    this.binaryDirectory = app.isPackaged
      ? path.join(process.resourcesPath, 'binaries')
      : path.join(process.cwd(), 'resources', 'binaries');
    this.script = app.isPackaged
      ? path.join(process.resourcesPath, 'engine', 'easyclip_engine.py')
      : path.join(process.cwd(), 'resources', 'engine', 'easyclip_engine.py');
  }

  private executable(): { command: string; prefix: string[] } {
    const executable = path.join(this.binaryDirectory, process.platform === 'win32' ? 'easyclip-engine.exe' : 'easyclip-engine');
    if (existsSync(executable)) return { command: executable, prefix: [] };
    if (!app.isPackaged && existsSync(this.script)) {
      return { command: process.env.EASYCLIP_PYTHON || (process.platform === 'win32' ? 'python' : 'python3'), prefix: [this.script] };
    }
    throw new Error(`Local AI engine is missing: ${executable}`);
  }

  private run(args: string[], onProgress?: (event: EngineProgress) => void, jobId?: string, secretEnv?: Record<string, string>): Promise<EngineResult> {
    const executable = this.executable();
    return new Promise((resolve, reject) => {
      const child = spawn(executable.command, [...executable.prefix, ...args], {
        windowsHide: true,
        env: {
          ...process.env,
          PATH: `${this.binaryDirectory}${path.delimiter}${process.env.PATH ?? ''}`,
          PYTHONUTF8: '1',
          HF_HOME: path.join(this.cacheDirectory, 'models'),
          ...secretEnv
        }
      });
      if (jobId) this.children.set(jobId, child);
      let stdout = '';
      let stderr = '';
      let currentStage = '';
      let modelWaitSeconds = 0;
      const heartbeat = setInterval(() => {
        if (currentStage !== 'model') return;
        modelWaitSeconds += 5;
        onProgress?.({
          event: 'progress',
          stage: 'model',
          percent: Math.min(95, 5 + modelWaitSeconds / 3),
          detail: `Loading the speech model (${String(modelWaitSeconds)}s). The first run also downloads it.`
        });
      }, 5_000);
      child.stdout.setEncoding('utf8');
      child.stderr.setEncoding('utf8');
      child.stdout.on('data', (value: string) => { stdout += value; });
      child.stderr.on('data', (value: string) => {
        stderr += value;
        for (const line of value.split(/\r?\n/)) {
          if (!line.trim()) continue;
          try {
            const event = JSON.parse(line) as EngineProgress;
            if (event.stage) currentStage = event.stage;
            onProgress?.(event);
          } catch { /* Native libraries can write diagnostics to stderr. */ }
        }
      });
      child.once('error', (error) => {
        clearInterval(heartbeat);
        if (jobId) this.children.delete(jobId);
        reject(new Error(`Unable to start local AI engine: ${error.message}`));
      });
      child.once('close', (code) => {
        clearInterval(heartbeat);
        if (jobId) this.children.delete(jobId);
        const line = stdout.trim().split(/\r?\n/).filter(Boolean).at(-1);
        if (!line) { reject(new Error(`Local AI engine returned no result${stderr ? `: ${stderr.trim()}` : ''}`)); return; }
        try {
          const result = JSON.parse(line) as EngineResult;
          if (code !== 0 || !result.ok) reject(new Error(result.error || `Local AI engine exited with code ${String(code)}`));
          else resolve(result);
        } catch (error: unknown) {
          reject(new Error(`Invalid local AI response: ${error instanceof Error ? error.message : String(error)}`));
        }
      });
    });
  }

  async status(): Promise<LocalEngineStatus> {
    try {
      const result = await this.run(['status']);
      return {
        available: true,
        engineVersion: result.engineVersion,
        cudaAvailable: result.cudaAvailable ?? false,
        recommendedModels: result.recommendedModels ?? [...allowedModels]
      };
    } catch (error: unknown) {
      return {
        available: false,
        cudaAvailable: false,
        recommendedModels: [...allowedModels],
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }

  async models(): Promise<LocalModelInfo[]> {
    return (await this.run(['models'])).models ?? [];
  }

  async prepareModel(model: string, onProgress?: (event: EngineProgress) => void): Promise<LocalModelInfo[]> {
    if (!allowedModels.has(model)) throw new Error(`Unsupported Whisper model: ${model}`);
    return (await this.run(['prepare-model', '--model', model], onProgress)).models ?? [];
  }

  async deleteModel(model: string): Promise<LocalModelInfo[]> {
    if (!allowedModels.has(model)) throw new Error(`Unsupported Whisper model: ${model}`);
    return (await this.run(['delete-model', '--model', model])).models ?? [];
  }

  cancel(jobId: string): boolean {
    const child = this.children.get(jobId);
    if (!child) return false;
    return child.kill();
  }

  async diarize(
    input: string,
    outputDirectory: string,
    token: string,
    options: { minSpeakers?: number; maxSpeakers?: number; jobId?: string },
    onProgress?: (event: EngineProgress) => void
  ): Promise<SpeakerTimeline> {
    if (!token.startsWith('hf_')) throw new Error('Professional speaker-model access is not configured');
    const result = await this.run([
      'diarize', '--input', input, '--output-dir', outputDirectory,
      '--cache-dir', this.cacheDirectory,
      '--min-speakers', String(options.minSpeakers ?? 1),
      '--max-speakers', String(options.maxSpeakers ?? 4)
    ], onProgress, options.jobId, { HF_TOKEN: token });
    return { speakers: result.speakers ?? [], turns: result.turns ?? [] };
  }

  async analyze(
    input: string,
    outputDirectory: string,
    options: { model: string; language: string; targetDuration: number; clipCount: number; jobId?: string },
    onProgress?: (event: EngineProgress) => void
  ): Promise<LocalHighlight[]> {
    if (!allowedModels.has(options.model)) throw new Error(`Unsupported Whisper model: ${options.model}`);
    const result = await this.run([
      'analyze', '--input', input, '--output-dir', outputDirectory,
      '--model', options.model, '--language', options.language,
      '--target-duration', String(Math.max(15, Math.min(180, options.targetDuration))),
      '--clip-count', String(Math.max(1, Math.min(30, options.clipCount))),
      '--cache-dir', this.cacheDirectory
    ], onProgress, options.jobId);
    if (!result.highlights?.length) throw new Error('Local AI did not find any highlight candidates');
    return result.highlights;
  }
}
