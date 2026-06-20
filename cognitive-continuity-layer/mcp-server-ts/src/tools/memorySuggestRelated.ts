import { MemoryEngineClient } from "../client";
import { SuggestRelatedSchema } from "../schemas/memorySchemas";

export async function handleMemorySuggestRelated(client: MemoryEngineClient, args: any) {
  const validatedArgs = SuggestRelatedSchema.parse(args);
  const result = await client.suggestRelated(validatedArgs);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
}
