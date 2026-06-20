import { MemoryEngineClient } from "../client";
import { SearchMemorySchema } from "../schemas/memorySchemas";

export async function handleMemorySearch(client: MemoryEngineClient, args: any) {
  const validatedArgs = SearchMemorySchema.parse(args);
  const result = await client.searchMemory(validatedArgs);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
}
