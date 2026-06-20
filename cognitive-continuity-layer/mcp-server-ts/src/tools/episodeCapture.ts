import { MemoryEngineClient } from "../client";
import { EpisodeCaptureSchema } from "../schemas/memorySchemas";

export async function handleEpisodeCapture(client: MemoryEngineClient, args: any) {
  const validatedArgs = EpisodeCaptureSchema.parse(args);
  const result = await client.captureEpisode(validatedArgs);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
}
