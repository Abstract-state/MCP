import { config } from './config';

export class MemoryEngineClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = config.memoryEngineUrl;
  }

  async post(path: string, body: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        throw new Error(`API Request Failed: ${response.status} ${response.statusText}`);
      }
      throw new Error(`API Error: ${JSON.stringify(errorData)}`);
    }

    return response.json();
  }

  async saveMemory(data: any) {
    return this.post('/memory/save', data);
  }

  async searchMemory(data: any) {
    return this.post('/memory/search', data);
  }

  async suggestRelated(data: any) {
    return this.post('/memory/suggest', data);
  }

  async getContextBundle(data: any) {
    return this.post('/context/bundle', data);
  }

  async captureEpisode(data: any) {
    return this.post('/episode/capture', data);
  }

  async analyzeEpisode(data: any) {
    return this.post('/episode/analyze', data);
  }

  async refinePreview(data: any) {
    return this.post('/prompt/refine-preview', data);
  }

  async refineConfirm(data: any) {
    return this.post('/prompt/refine-confirm', data);
  }
}
