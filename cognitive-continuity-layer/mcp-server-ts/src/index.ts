import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import {
  SaveMemorySchema,
  SearchMemorySchema,
  SuggestRelatedSchema,
  ApplyContextBundleSchema,
  EpisodeCaptureSchema,
  EpisodeAnalyzeSchema,
  PromptRefinePreviewSchema,
  PromptRefineConfirmSchema,
  CommunicationLearnSchema,
  CommunicationSearchSchema,
  ProfileGetSchema
} from "./schemas/memorySchemas";
import { MemoryEngineClient } from "./client";

const client = new MemoryEngineClient();

export const server = new Server(
  {
    name: "cognitive_continuity_mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "memory.save",
        description: "Save a new memory to the cognitive continuity layer",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            type: { type: "string" },
            title: { type: "string" },
            summary: { type: "string" },
            content: { type: "string" },
            scope: { type: "string" },
            status: { type: "string" }
          },
          required: ["user_id", "workspace_id", "type", "title", "summary", "content", "scope", "status"]
        }
      },
      {
        name: "memory.search",
        description: "Search for existing memories",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            query: { type: "string" }
          },
          required: ["user_id", "workspace_id", "query"]
        }
      },
      {
        name: "memory.suggest_related",
        description: "Suggest related context based on the current query",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            current_query: { type: "string" }
          },
          required: ["user_id", "workspace_id", "current_query"]
        }
      },
      {
        name: "memory.apply_context_bundle",
        description: "Fetch a context bundle of instructions for specific memories",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            memory_ids: { type: "array", items: { type: "string" } }
          },
          required: ["user_id", "workspace_id", "memory_ids"]
        }
      },
      {
        name: "profile.get",
        description: "Get user profile and global preferences",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" }
          },
          required: ["user_id", "workspace_id"]
        }
      },
      {
        name: "episode.capture",
        description: "Capture a conversation turn for an episode",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            episode_id: { type: "string" },
            turn: { type: "object", properties: { turn_id: { type: "string" }, role: { type: "string" }, message: { type: "string" } }, required: ["turn_id", "role", "message"] }
          },
          required: ["user_id", "workspace_id", "episode_id", "turn"]
        }
      },
      {
        name: "episode.analyze",
        description: "Analyze an episode for friction and acceptance",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            episode_id: { type: "string" }
          },
          required: ["user_id", "workspace_id", "episode_id"]
        }
      },
      {
        name: "prompt.refine_preview",
        description: "Generate a prompt refinement preview based on behavioral history",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            prompt: { type: "string" }
          },
          required: ["user_id", "workspace_id", "prompt"]
        }
      },
      {
        name: "prompt.refine_confirm",
        description: "Confirm or reject a prompt refinement proposal",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            original_prompt: { type: "string" },
            approved_prompt: { type: "string" },
            accepted: { type: "boolean" }
          },
          required: ["user_id", "workspace_id", "original_prompt", "approved_prompt", "accepted"]
        }
      },
      {
        name: "communication.learn",
        description: "Explicitly learn a communication pattern",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            pattern: { type: "string" },
            meaning: { type: "array", items: { type: "string" } }
          },
          required: ["user_id", "workspace_id", "pattern", "meaning"]
        }
      },
      {
        name: "communication.search",
        description: "Search for communication patterns",
        inputSchema: {
          type: "object",
          properties: {
            user_id: { type: "string" },
            workspace_id: { type: "string" },
            query: { type: "string" }
          },
          required: ["user_id", "workspace_id", "query"]
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    switch (request.params.name) {
      case "memory.save": {
        const args = SaveMemorySchema.parse(request.params.arguments);
        const result = await client.saveMemory(args);
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      }
      case "memory.search": {
        const args = SearchMemorySchema.parse(request.params.arguments);
        const result = await client.searchMemory(args);
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      }
      case "memory.suggest_related": {
        const args = SuggestRelatedSchema.parse(request.params.arguments);
        const result = await client.suggestRelated(args);
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      }
      case "memory.apply_context_bundle": {
        const args = ApplyContextBundleSchema.parse(request.params.arguments);
        const result = await client.getContextBundle(args);
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      }
      case "profile.get": {
        // Placeholder for now
        return { content: [{ type: "text", text: JSON.stringify({ profile: { user_id: request.params.arguments?.user_id, preferences: [] } }) }] };
      }
      case "episode.capture": {
        const args = EpisodeCaptureSchema.parse(request.params.arguments);
        const result = await client.captureEpisode(args);
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      }
      case "episode.analyze": {
        const args = EpisodeAnalyzeSchema.parse(request.params.arguments);
        const result = await client.analyzeEpisode(args);
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      }
      case "prompt.refine_preview": {
        const args = PromptRefinePreviewSchema.parse(request.params.arguments);
        const result = await client.refinePreview(args);
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      }
      case "prompt.refine_confirm": {
        const args = PromptRefineConfirmSchema.parse(request.params.arguments);
        const result = await client.refineConfirm(args);
        return { content: [{ type: "text", text: JSON.stringify(result) }] };
      }
      case "communication.learn":
      case "communication.search": {
        return { content: [{ type: "text", text: JSON.stringify({ status: "not_implemented_yet_in_poc" }) }] };
      }
      default:
        throw new Error(`Unknown tool: ${request.params.name}`);
    }
  } catch (error: any) {
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Cognitive Continuity MCP Server running on stdio");
}

if (require.main === module) {
  main().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
  });
}
