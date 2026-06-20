import { z } from "zod";

export const SaveMemorySchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  type: z.enum(["preference", "communication_pattern", "task_context", "accepted_pattern", "rejected_pattern", "playbook", "constraint", "decision"]),
  title: z.string().max(120),
  summary: z.string().max(500),
  content: z.string().max(5000),
  tags: z.array(z.string()).max(20).optional(),
  linked_entities: z.array(z.object({ type: z.string(), id: z.string() })).max(20).optional(),
  scope: z.enum(["private", "project", "workspace", "team", "organization"]),
  status: z.enum(["draft", "suggested", "approved", "rejected", "archived"])
});

export const SearchMemorySchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  query: z.string().min(3),
  max_results: z.number().min(1).max(20).optional().default(5),
  filters: z.object({
    status: z.string().optional(),
    type: z.string().optional()
  }).optional()
});

export const SuggestRelatedSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  current_query: z.string().min(3),
  linked_ids: z.array(z.string()).optional(),
  max_results: z.number().min(1).max(10).optional().default(3)
});

export const ApplyContextBundleSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  memory_ids: z.array(z.string()).min(1).max(5)
});

export const EpisodeCaptureSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  episode_id: z.string(),
  turn: z.object({
    turn_id: z.string(),
    role: z.string(),
    message: z.string()
  }),
  assistant_client: z.string().optional(),
  model_used: z.string().optional()
});

export const EpisodeAnalyzeSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  episode_id: z.string()
});

export const PromptRefinePreviewSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  prompt: z.string(),
  linked_ids: z.array(z.string()).optional()
});

export const PromptRefineConfirmSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  original_prompt: z.string(),
  approved_prompt: z.string(),
  accepted: z.boolean()
});

export const CommunicationLearnSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  pattern: z.string(),
  meaning: z.array(z.string())
});

export const CommunicationSearchSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string(),
  query: z.string()
});

export const ProfileGetSchema = z.object({
  user_id: z.string(),
  workspace_id: z.string()
});
