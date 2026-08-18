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

interface EngineResult {
  ok: boolean;
  error?: string;
  highlights?: LocalHighlight[];
  engineVersion?: string;
  cudaAvailable?: boolean;
  recommendedModels?: string[];
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

  constructor() {
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

  private run(args: string[], onProgress?: (event: EngineProgress) => void): Promise<EngineResult> {
    const executable = this.executable();
    return new Promise((resolve, reject) => {
      const child = spawn(executable.command, [...executable.prefix, ...args], {
        windowsHide: true,
        env: {
          ...process.env,
          PATH: `${this.binaryDirectory}${path.delimiter}${process.env.PATH ?? ''}`,
          PYTHONUTF8: '1'
        }
      });
      let stdout = '';
      let stderr = '';
      child.stdout.setEncoding('utf8');
      child.stderr.setEncoding('utf8');
      child.stdout.on('data', (value: string) => { stdout += value; });
      child.stderr.on('data', (value: string) => {
        stderr += value;
        for (const line of value.split(/\r?\n/)) {
          if (!line.trim()) continue;
          try { onProgress?.(JSON.parse(line) as EngineProgress); }
          catch { /* Native libraries can write diagnostics to stderr. */ }
        }
      });
      child.once('error', (error) => reject(new Error(`Unable to start local AI engine: ${error.message}`)));
      child.once('close', (code) => {
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

  async analyze(
    input: string,
    outputDirectory: string,
    options: { model: string; language: string; targetDuration: number; clipCount: number },
    onProgress?: (event: EngineProgress) => void
  ): Promise<LocalHighlight[]> {
    if (!allowedModels.has(options.model)) throw new Error(`Unsupported Whisper model: ${options.model}`);
    const result = await this.run([
      'analyze', '--input', input, '--output-dir', outputDirectory,
      '--model', options.model, '--language', options.language,
      '--target-duration', String(Math.max(15, Math.min(180, options.targetDuration))),
      '--clip-count', String(Math.max(1, Math.min(30, options.clipCount)))
    ], onProgress);
    if (!result.highlights?.length) throw new Error('Local AI did not find any highlight candidates');
    return result.highlights;
  }
}
