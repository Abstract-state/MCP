import { MemoryEngineClient } from "../client";
import { SaveMemorySchema } from "../schemas/memorySchemas";

export async function handleMemorySave(client: MemoryEngineClient, args: any) {
  const validatedArgs = SaveMemorySchema.parse(args);
  const result = await client.saveMemory(validatedArgs);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
}
