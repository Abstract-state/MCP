# API Contract

## 1. Legacy Memory APIs
- `POST /memory/save`: Upsert explicit memories to `cognitive_memories`.
- `POST /memory/search`: Raw vector similarity retrieval.
- `POST /memory/suggest`: Scoring-based threshold retrieval.
- `POST /context/bundle`: Consolidate retrieved IDs into actionable LLM instruction bundles.

## 2. Phase 1 Behavioral APIs

### `POST /episode/capture`
Captures a single conversation turn and appends it to an episode.
**Request**:
```json
{
  "user_id": "demo",
  "workspace_id": "corp",
  "episode_id": "ep_1",
  "turn": {
    "turn_id": "t_1",
    "role": "user",
    "message": "Fix the query again."
  }
}
```
**Response**: `{"status": "captured", "episode_id": "ep_1"}`

### `POST /episode/analyze`
Analyzes a captured episode for acceptance signals, recalculates friction scores, and structures it for retrieval.
**Request**:
```json
{
  "user_id": "demo",
  "workspace_id": "corp",
  "episode_id": "ep_1"
}
```
**Response**: `{"episode_id": "ep_1", "friction_score": 7.5, "accepted": true, ...}`

### `POST /prompt/refine-preview`
Generates a prompt enhancement proposal based on behavioral history, utilizing the Hybrid Ranker.
**Request**:
```json
{
  "user_id": "demo",
  "workspace_id": "corp",
  "prompt": "minimal changes please"
}
```
**Response**: 
```json
{
  "original_prompt": "minimal changes please",
  "proposal": {
    "interpreted_meaning": ["Detected behavioral instruction: 'minimal changes'"],
    "retrieved_context": ["Always use variables in DAX..."],
    "refined_prompt": "minimal changes please\n\n# Context Applied:\n- Always use variables in DAX..."
  }
}
```

### `POST /prompt/refine-confirm`
Logs the user's explicit approval or rejection of the prompt refinement.
**Request**:
```json
{
  "user_id": "demo",
  "workspace_id": "corp",
  "original_prompt": "minimal changes please",
  "approved_prompt": "minimal changes please\n\n# Context Applied...",
  "accepted": true
}
```
**Response**: `{"status": "confirmed"}`
