import axios, { AxiosError, type AxiosInstance } from 'axios';

export interface OllamaStatus { running: boolean; models: string[]; error?: string }

function message(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.code === 'ECONNREFUSED') return 'Ollama is not running on the configured address';
    if (error.code === 'ETIMEDOUT' || error.code === 'ECONNABORTED') return 'Ollama did not respond before the timeout';
    return error.response?.data ? JSON.stringify(error.response.data) : error.message;
  }
  return error instanceof Error ? error.message : String(error);
}

export class OllamaService {
  private readonly http: AxiosInstance;

  constructor(endpoint = 'http://127.0.0.1:11434') {
    let parsed: URL;
    try { parsed = new URL(endpoint); }
    catch { throw new Error('The Ollama endpoint is not a valid URL'); }
    if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('The Ollama endpoint must use HTTP or HTTPS');
    this.http = axios.create({ baseURL: parsed.toString().replace(/\/$/, ''), timeout: 2_000 });
  }

  async status(): Promise<OllamaStatus> {
    try {
      const response = await this.http.get<{ models?: Array<{ name?: string }> }>('/api/tags');
      const models = (response.data.models ?? []).map((model) => model.name?.trim()).filter((name): name is string => Boolean(name));
      return { running: true, models };
    } catch (error: unknown) {
      return { running: false, models: [], error: message(error) };
    }
  }

  async generate(model: string, prompt: string): Promise<string> {
    if (!model.trim()) throw new Error('Select an Ollama model before analysis');
    if (!prompt.trim()) throw new Error('The Ollama prompt is empty');
    try {
      const response = await this.http.post<{ response?: string }>('/api/generate', {
        model, prompt, stream: false, format: 'json', options: { temperature: 0.7, num_predict: 2048 }
      }, { timeout: 300_000 });
      const result = response.data.response?.trim();
      if (!result) throw new Error('Ollama returned an empty response');
      return result;
    } catch (error: unknown) {
      throw new Error(`Ollama analysis failed: ${message(error)}`);
    }
  }

  async pull(model: string, onProgress: (percent: number, status: string) => void): Promise<void> {
    if (!model.trim()) throw new Error('Select an Ollama model before downloading');
    try {
      const response = await this.http.post<ReadableStream<Uint8Array>>('/api/pull', { name: model, stream: true }, { responseType: 'stream', timeout: 0 });
      const stream = response.data as unknown as NodeJS.ReadableStream;
      let text = '';
      for await (const chunk of stream) {
        text += String(chunk);
        const lines = text.split('\n');
        text = lines.pop() ?? '';
        for (const line of lines) {
          if (!line) continue;
          const data = JSON.parse(line) as { completed?: number; total?: number; status: string; error?: string };
          if (data.error) throw new Error(data.error);
          onProgress(data.total ? Math.round((data.completed ?? 0) / data.total * 100) : 0, data.status);
        }
      }
    } catch (error: unknown) {
      throw new Error(`Ollama model download failed: ${message(error)}`);
    }
  }
}
