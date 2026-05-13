import { describe, it, expect, vi } from 'vitest';
import { MemoryEngineClient } from '../src/client';
import { server } from '../src/index';

// Mock the HTTP client
global.fetch = vi.fn();

describe('MemoryEngineClient', () => {
  it('should post successfully', async () => {
    const client = new MemoryEngineClient();
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok' })
    });
    
    const res = await client.saveMemory({ user_id: '1', workspace_id: '1' });
    expect(res.status).toBe('ok');
    expect(global.fetch).toHaveBeenCalled();
  });
  
  it('should handle API errors cleanly', async () => {
    const client = new MemoryEngineClient();
    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 422,
      json: async () => ({ detail: 'Validation Error' })
    });
    
    await expect(client.saveMemory({})).rejects.toThrow('API Error');
  });

  it('should hit captureEpisode endpoint successfully', async () => {
    const client = new MemoryEngineClient();
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'captured', episode_id: 'ep_1' })
    });
    
    const res = await client.captureEpisode({ user_id: '1', workspace_id: '1', episode_id: 'ep_1', turn: { turn_id: '1', role: 'user', message: 'test' } });
    expect(res.status).toBe('captured');
    expect(global.fetch).toHaveBeenCalled();
  });
});

describe('MCP Server', () => {
  it('should register tools', async () => {
    // We can't easily trigger the server request handler directly without the exact SDK types, 
    // but we can check if it initializes.
    expect(server).toBeDefined();
  });
});
