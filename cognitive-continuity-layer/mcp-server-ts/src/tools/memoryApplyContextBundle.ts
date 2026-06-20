import { MemoryEngineClient } from "../client";
import { ApplyContextBundleSchema } from "../schemas/memorySchemas";

export async function handleMemoryApplyContextBundle(client: MemoryEngineClient, args: any) {
  const validatedArgs = ApplyContextBundleSchema.parse(args);
  const result = await client.getContextBundle(validatedArgs);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
}
