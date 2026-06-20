import { MemoryEngineClient } from "../client";
import { ProfileGetSchema } from "../schemas/memorySchemas";

export async function handleProfileGet(client: MemoryEngineClient, args: any) {
  const validatedArgs = ProfileGetSchema.parse(args);
  const result = await client.getProfile(validatedArgs);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
}
