import { createReadStream, statSync } from 'node:fs';
import { google } from 'googleapis';
import axios, { isAxiosError } from 'axios';
import type { AuthService } from './AuthService';
import type { UploadInput } from '../types';
import type { QuotaService } from './QuotaService';

const CHUNK_SIZE = 10 * 1024 * 1024; // Resumable uploads are sent in 10 MB chunks so interruptions lose at most one chunk.

export interface ResumableState { sessionUri?: string; offset?: number }
export interface UploadCallbacks {
  onProgress: (percent: number) => void;
  /** Called whenever the resumable session URI or committed offset changes, so callers can checkpoint it. */
  onCheckpoint?: (state: Required<ResumableState>) => void;
  signal?: AbortSignal;
}

async function readChunk(file: string, start: number, end: number): Promise<Buffer> {
  const stream = createReadStream(file, { start, end: end - 1 });
  const parts: Buffer[] = [];
  for await (const part of stream) parts.push(part as Buffer);
  return Buffer.concat(parts);
}

export class YouTubeService {
  constructor(private readonly auth: AuthService, private readonly quota: QuotaService) {}

  private async accessToken(): Promise<string> {
    const client = await this.auth.authenticatedClient();
    const { token } = await client.getAccessToken();
    if (!token) throw new Error('Unable to obtain a Google access token');
    return token;
  }

  private async createSession(size: number, input: UploadInput, token: string): Promise<string> {
    const response = await axios.post(
      'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status',
      {
        snippet: {
          title: input.title ?? 'Uploaded video',
          description: input.description ?? '',
          tags: input.tags ?? [],
          categoryId: input.categoryId ?? '22'
        },
        status: { privacyStatus: input.privacy ?? 'unlisted', selfDeclaredMadeForKids: input.madeForKids ?? false }
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'X-Upload-Content-Length': String(size),
          'X-Upload-Content-Type': 'video/*'
        }
      }
    );
    const location = (response.headers as Record<string, string>).location;
    if (!location) throw new Error('YouTube did not return a resumable session URI');
    return location;
  }

  /** Asks the resumable endpoint how many bytes it has already committed. */
  private async committedOffset(sessionUri: string, size: number, token: string): Promise<number> {
    try {
      await axios.put(sessionUri, undefined, {
        headers: { Authorization: `Bearer ${token}`, 'Content-Range': `bytes */${String(size)}` },
        validateStatus: (status) => status === 308
      });
      return 0;
    } catch (error: unknown) {
      if (isAxiosError(error) && error.response?.status === 308) {
        const range = (error.response.headers as Record<string, string>).range;
        const match = range ? /bytes=0-(\d+)/.exec(range) : null;
        return match?.[1] ? Number(match[1]) + 1 : 0;
      }
      if (isAxiosError(error) && (error.response?.status === 200 || error.response?.status === 201)) return size;
      return 0;
    }
  }

  async upload(file: string, input: UploadInput, callbacks: UploadCallbacks, resume: ResumableState = {}): Promise<{ id: string; url: string }> {
    const cost = 1600 + (input.thumbnailPath ? 50 : 0);
    this.quota.require(cost);
    const size = statSync(file).size;
    const token = await this.accessToken();
    let sessionUri = resume.sessionUri;
    let offset = 0;
    if (sessionUri) {
      offset = await this.committedOffset(sessionUri, size, token);
    } else {
      sessionUri = await this.createSession(size, input, token);
      callbacks.onCheckpoint?.({ sessionUri, offset: 0 });
    }
    let videoId: string | undefined;
    while (offset < size) {
      if (callbacks.signal?.aborted) throw new Error('Cancelled');
      const end = Math.min(offset + CHUNK_SIZE, size);
      const chunk = await readChunk(file, offset, end);
      try {
        const response = await axios.put(sessionUri, chunk, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Range': `bytes ${String(offset)}-${String(end - 1)}/${String(size)}`,
            'Content-Type': 'video/*'
          },
          maxBodyLength: Infinity,
          signal: callbacks.signal,
          validateStatus: (status) => status === 308 || status === 200 || status === 201
        });
        if (response.status === 200 || response.status === 201) {
          const body = response.data as { id?: string };
          videoId = body.id;
          offset = size;
        } else {
          const range = (response.headers as Record<string, string>).range;
          const match = range ? /bytes=0-(\d+)/.exec(range) : null;
          offset = match?.[1] ? Number(match[1]) + 1 : end;
        }
      } catch (error: unknown) {
        if (callbacks.signal?.aborted) throw new Error('Cancelled');
        throw error instanceof Error ? error : new Error(String(error));
      }
      callbacks.onCheckpoint?.({ sessionUri, offset });
      callbacks.onProgress(Math.min(100, Math.round(offset / size * 100)));
    }
    if (!videoId) throw new Error('YouTube did not return a video ID');
    if (input.thumbnailPath) {
      const client = await this.auth.authenticatedClient();
      const youtube = google.youtube({ version: 'v3', auth: client });
      await youtube.thumbnails.set({ videoId, media: { body: createReadStream(input.thumbnailPath) } });
    }
    this.quota.consume(cost);
    return { id: videoId, url: `https://youtu.be/${videoId}` };
  }
}
