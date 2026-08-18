import axios, { AxiosError } from 'axios';
import type { CredentialVault } from './CredentialVault';

const SERVICE = 'VioletCutProfessionalAI';
const ACCOUNT = 'HuggingFaceReadToken';
const requiredRepositories = [
  'pyannote/speaker-diarization-3.1',
  'pyannote/segmentation-3.0'
] as const;

export interface HuggingFaceState {
  configured: boolean;
  verified: boolean;
  username?: string;
  repositories: Array<{ id: string; accessible: boolean }>;
  error?: string;
}

function safeMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response?.status === 401) return 'The access token is invalid or expired';
    if (error.response?.status === 403) return 'The account has not accepted the model terms';
    if (error.response?.status === 404) return 'A required model repository is unavailable';
    if (error.code === 'ECONNABORTED') return 'The model service did not respond before the timeout';
  }
  return error instanceof Error ? error.message.replace(/hf_[A-Za-z0-9]+/g, '[redacted]') : 'Model access validation failed';
}

export class HuggingFaceService {
  constructor(private readonly vault: CredentialVault) {}

  private async token(): Promise<string | null> { return this.vault.get(SERVICE, ACCOUNT); }
  async accessToken(): Promise<string | null> { return this.token(); }

  private async verifyToken(token: string): Promise<HuggingFaceState> {
    if (!/^hf_[A-Za-z0-9]{20,}$/.test(token.trim())) throw new Error('The access token format is invalid');
    const headers = { Authorization: `Bearer ${token.trim()}` };
    const who = await axios.get<{ name?: string; fullname?: string }>('https://huggingface.co/api/whoami-v2', { headers, timeout: 15_000 });
    const repositories = await Promise.all(requiredRepositories.map(async (id) => {
      try {
        await axios.get(`https://huggingface.co/${id}/resolve/main/config.yaml`, {
          headers, timeout: 20_000, responseType: 'text', maxContentLength: 2_000_000
        });
        return { id, accessible: true };
      } catch { return { id, accessible: false }; }
    }));
    return {
      configured: true,
      verified: repositories.every((repository) => repository.accessible),
      username: who.data.name ?? who.data.fullname,
      repositories
    };
  }

  async state(validate = false): Promise<HuggingFaceState> {
    const token = await this.token();
    if (!token) return { configured: false, verified: false, repositories: requiredRepositories.map((id) => ({ id, accessible: false })) };
    if (!validate) return { configured: true, verified: false, repositories: requiredRepositories.map((id) => ({ id, accessible: false })) };
    try { return await this.verifyToken(token); }
    catch (error: unknown) {
      return { configured: true, verified: false, repositories: requiredRepositories.map((id) => ({ id, accessible: false })), error: safeMessage(error) };
    }
  }

  async save(token: string): Promise<HuggingFaceState> {
    const state = await this.verifyToken(token);
    if (!state.verified) throw new Error('Accept the terms for both required speaker models before saving the token');
    await this.vault.set(SERVICE, ACCOUNT, token.trim());
    return state;
  }

  async remove(): Promise<HuggingFaceState> {
    await this.vault.delete(SERVICE, ACCOUNT);
    return this.state();
  }
}
