import dotenv from 'dotenv';
dotenv.config();

export const config = {
  memoryEngineUrl: process.env.MEMORY_ENGINE_URL || 'http://localhost:8001',
};
