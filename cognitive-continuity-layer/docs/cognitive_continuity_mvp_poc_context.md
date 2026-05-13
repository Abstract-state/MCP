# Cognitive Continuity Layer for AI Assistants — MVP/POC Context Document

## 1. Project Summary

### Product Name
**Cognitive Continuity Layer for AI Assistants**

### Goal
Build an MCP-based memory and context intelligence server that helps AI assistants preserve continuity across chats, tasks, tools, and users. The MVP/POC focuses on storing user-approved context, retrieving similar memories, and suggesting relevant prior context before the assistant responds.

### Core Problem
Existing MCP tools in the corporate environment already retrieve project or repository context from markdown files, code repos, and environment metadata. However, they do not understand the user’s communication style, accepted patterns, repeated preferences, or previous task-specific instructions across chats.

This causes:

- repeated explanation across chats
- higher token usage
- incorrect assumptions by the assistant
- discarded AI responses
- user frustration
- inconsistent output format
- poor continuity across Copilot, IDE, and other AI assistant sessions

### MVP Hypothesis
If an assistant can retrieve user-approved prior task context and communication preferences, then response acceptance will improve and repeated explanation will reduce.

### MVP Scope
The MVP should prove three things:

1. A user can save reusable context manually.
2. The system can retrieve similar context using ChromaDB.
3. The assistant can suggest relevant previous context and ask for approval before applying it.

---

## 2. MVP Technology Stack

### Required Stack

| Area | Technology |
|---|---|
| MCP Server | TypeScript / Node.js |
| Memory Engine | Python |
| Vector Store | ChromaDB |
| Python API | FastAPI |
| Validation | Pydantic |
| Local Metadata | SQLite or Chroma metadata |
| Test Framework - TypeScript | Vitest or Jest |
| Test Framework - Python | Pytest |
| Package Management - TypeScript | npm or pnpm |
| Package Management - Python | pip + venv |

### Python Libraries

Installable Python libraries for POC:

```bash
pip install fastapi uvicorn chromadb pydantic python-dotenv pytest httpx rapidfuzz sentence-transformers
```

Optional libraries:

```bash
pip install sqlalchemy spacy nltk scikit-learn
```

### TypeScript Packages

```bash
npm install @modelcontextprotocol/sdk zod dotenv
npm install -D typescript ts-node vitest @types/node
```

---

## 3. High-Level Architecture

```text
AI Assistant / Copilot / Codex / Antigravity
        ↓
MCP Client
        ↓
TypeScript MCP Server
        ↓
HTTP API Call
        ↓
Python Memory Engine
        ↓
ChromaDB Persistent Store
```

### Component Responsibilities

#### TypeScript MCP Server
Responsible for:

- exposing MCP tools
- validating tool inputs
- communicating with Python memory engine
- returning structured context suggestions
- later serving UI resource cards

#### Python Memory Engine
Responsible for:

- saving memory
- querying ChromaDB
- ranking results
- filtering metadata
- generating context bundles
- exposing REST endpoints

#### ChromaDB
Responsible for:

- storing vector-searchable memory documents
- storing metadata such as user ID, workspace ID, tags, status, linked IDs, memory type, confidence, and timestamps

---

## 4. Repository Structure

```text
cognitive-continuity-layer/

  README.md
  .env.example
  docker-compose.yml

  mcp-server-ts/
    package.json
    tsconfig.json
    src/
      index.ts
      config.ts
      client/
        memoryEngineClient.ts
      tools/
        memorySave.ts
        memorySearch.ts
        memorySuggestRelated.ts
        memoryApplyContextBundle.ts
        profileGet.ts
      schemas/
        memorySchemas.ts
      utils/
        errors.ts
    tests/
      memorySave.test.ts
      memorySuggestRelated.test.ts
      memoryEngineClient.test.ts

  memory-engine-py/
    requirements.txt
    app/
      main.py
      config.py
      schemas.py
      chroma_store.py
      ranking.py
      context_bundle.py
      profile_service.py
      memory_service.py
    tests/
      test_memory_save.py
      test_memory_search.py
      test_memory_suggest.py
      test_ranking.py
      test_context_bundle.py

  docs/
    architecture.md
    api-contract.md
    test-plan.md
    demo-script.md
    agent-instructions.md
```

---

## 5. Core Concepts

### Memory Types

The MVP should support the following memory types:

```text
preference
communication_pattern
task_context
accepted_pattern
rejected_pattern
playbook
constraint
decision
```

### Memory Status

```text
draft
suggested
approved
rejected
archived
```

Only `approved` memories should be automatically eligible for context suggestions unless the request explicitly asks for draft or rejected memory.

### Memory Scope

```text
private
project
workspace
team
organization
```

For POC, start with:

```text
private
workspace
```

### Linked Entities

Memory can be linked to:

```text
jira_id
project_id
repo_name
branch_name
file_path
chat_id
user_label
customer_id
document_id
```

---

## 6. ChromaDB Collection Design

### Collection Name

```text
cognitive_memories
```

### Document Text

The document stored in Chroma should be a search-optimized text body:

```text
Title: Minimal DAX fix style
Type: task_context
Summary: User prefers DAX fixes with minimal logic changes.
Content: When fixing DAX queries, preserve measure names, avoid unnecessary refactoring, return the corrected DAX first, then provide short explanation.
Tags: dax, bi, minimal-change, formatting
Linked Entities: BI-482, analytics-reporting
```

### Metadata Example

```json
{
  "memory_id": "mem_001",
  "user_id": "u_001",
  "workspace_id": "corp_ws",
  "scope": "private",
  "type": "task_context",
  "title": "Minimal DAX fix style",
  "tags": "dax,bi,minimal-change,formatting",
  "linked_ids": "BI-482,analytics-reporting",
  "status": "approved",
  "confidence": 0.91,
  "created_at": "2026-05-11T10:00:00Z",
  "updated_at": "2026-05-11T10:00:00Z",
  "usage_count": 0,
  "accepted_count": 0,
  "rejected_count": 0
}
```

### Important ChromaDB Notes

- Use persistent ChromaDB client for POC.
- Use explicit IDs for upsert.
- Store full memory content in the Chroma document.
- Store filterable attributes in metadata.
- Avoid storing sensitive raw chats without approval.
- For large original source data, store only references and summarized memory.

---

## 7. Python Memory Engine API

### Base URL

```text
http://localhost:8001
```

### Endpoint: Save Memory

```http
POST /memory/save
```

Request:

```json
{
  "user_id": "u_001",
  "workspace_id": "corp_ws",
  "type": "task_context",
  "title": "Minimal DAX fix style",
  "summary": "User prefers minimal logic changes for DAX fixes.",
  "content": "Preserve measure names, avoid refactoring, return corrected DAX first.",
  "tags": ["dax", "minimal-change", "formatting"],
  "linked_entities": [
    { "type": "jira", "id": "BI-482" },
    { "type": "project", "id": "analytics-reporting" }
  ],
  "scope": "private",
  "status": "approved"
}
```

Response:

```json
{
  "memory_id": "mem_001",
  "status": "saved"
}
```

### Endpoint: Search Memory

```http
POST /memory/search
```

Request:

```json
{
  "user_id": "u_001",
  "workspace_id": "corp_ws",
  "query": "fix DAX query same as last time",
  "max_results": 5,
  "filters": {
    "status": "approved",
    "type": "task_context"
  }
}
```

Response:

```json
{
  "results": [
    {
      "memory_id": "mem_001",
      "title": "Minimal DAX fix style",
      "summary": "User prefers minimal logic changes for DAX fixes.",
      "score": 0.89,
      "metadata": {
        "type": "task_context",
        "status": "approved",
        "linked_ids": "BI-482,analytics-reporting"
      }
    }
  ]
}
```

### Endpoint: Suggest Related Context

```http
POST /memory/suggest
```

Request:

```json
{
  "user_id": "u_001",
  "workspace_id": "corp_ws",
  "current_query": "Can you fix this DAX measure using the previous style?",
  "linked_ids": ["BI-482"],
  "max_results": 3
}
```

Response:

```json
{
  "suggestions": [
    {
      "memory_id": "mem_001",
      "title": "Minimal DAX fix style",
      "reason": "Matched DAX task type and linked Jira BI-482.",
      "confidence": 0.92,
      "preview": "Preserve measure names, avoid refactoring, return corrected DAX first.",
      "requires_approval": true
    }
  ]
}
```

### Endpoint: Build Context Bundle

```http
POST /context/bundle
```

Request:

```json
{
  "user_id": "u_001",
  "workspace_id": "corp_ws",
  "memory_ids": ["mem_001"]
}
```

Response:

```json
{
  "context_bundle": {
    "bundle_id": "bundle_001",
    "instructions": [
      "When fixing DAX, make minimal changes only.",
      "Preserve existing measure names.",
      "Return corrected DAX first, then a short explanation."
    ],
    "source_memory_ids": ["mem_001"]
  }
}
```

### Endpoint: Get Profile

```http
POST /profile/get
```

Request:

```json
{
  "user_id": "u_001",
  "workspace_id": "corp_ws"
}
```

Response:

```json
{
  "profile": {
    "user_id": "u_001",
    "preferences": [
      "Prefer concise responses.",
      "Prefer code or answer first, explanation second.",
      "Avoid major refactoring unless explicitly requested."
    ]
  }
}
```

---

## 8. MCP Tool Specification

### Tool: memory.save

Purpose:
Save reusable user-approved context.

Input:

```json
{
  "user_id": "string",
  "workspace_id": "string",
  "type": "string",
  "title": "string",
  "summary": "string",
  "content": "string",
  "tags": ["string"],
  "linked_entities": [
    { "type": "string", "id": "string" }
  ],
  "scope": "private",
  "status": "approved"
}
```

Output:

```json
{
  "memory_id": "string",
  "status": "saved"
}
```

Validation:

- `user_id` required
- `workspace_id` required
- `title` required and max 120 characters
- `summary` required and max 500 characters
- `content` required
- `type` must be valid memory type
- `scope` must be valid scope
- `status` must be valid status

### Tool: memory.search

Purpose:
Search previously saved memory.

Input:

```json
{
  "user_id": "string",
  "workspace_id": "string",
  "query": "string",
  "max_results": 5,
  "filters": {
    "status": "approved",
    "type": "task_context"
  }
}
```

Output:

```json
{
  "results": []
}
```

Validation:

- query required
- max_results must be between 1 and 20
- filters optional

### Tool: memory.suggest_related

Purpose:
Find context likely relevant to the current user request.

Input:

```json
{
  "user_id": "string",
  "workspace_id": "string",
  "current_query": "string",
  "linked_ids": ["string"],
  "max_results": 3
}
```

Output:

```json
{
  "suggestions": [
    {
      "memory_id": "string",
      "title": "string",
      "reason": "string",
      "confidence": 0.0,
      "preview": "string",
      "requires_approval": true
    }
  ]
}
```

Validation:

- current_query required
- max_results defaults to 3
- suggestions must not include rejected or archived memories unless explicitly requested

### Tool: memory.apply_context_bundle

Purpose:
Build a compact assistant-ready instruction bundle from approved memory IDs.

Input:

```json
{
  "user_id": "string",
  "workspace_id": "string",
  "memory_ids": ["string"]
}
```

Output:

```json
{
  "bundle_id": "string",
  "instructions": ["string"],
  "source_memory_ids": ["string"]
}
```

Validation:

- memory_ids required
- only approved memory can be bundled by default
- bundle must be concise
- bundle must include source memory IDs

### Tool: profile.get

Purpose:
Return user communication profile.

Input:

```json
{
  "user_id": "string",
  "workspace_id": "string"
}
```

Output:

```json
{
  "preferences": ["string"]
}
```

---

## 9. Retrieval and Ranking Logic

### MVP Ranking Formula

```text
final_score =
  0.70 * vector_similarity
+ 0.15 * linked_id_match
+ 0.10 * approved_status_boost
+ 0.05 * recency_boost
```

### Linked ID Match

If the current request contains or provides a matching linked ID such as Jira ID, branch name, repo name, or project label, boost the result.

### Status Boost

```text
approved = +0.10
suggested = +0.02
rejected = excluded by default
archived = excluded by default
```

### Recency Boost

For POC:

```text
used within 7 days = +0.05
used within 30 days = +0.03
older = +0.00
```

### Minimum Threshold

Only suggest memories with:

```text
final_score >= 0.70
```

If no result meets threshold:

```json
{
  "suggestions": [],
  "message": "No strong related context found."
}
```

---

## 10. User Approval Flow

### Required Behavior

The system must not silently apply memory unless the context is explicitly pinned or the user has enabled auto-apply.

Default flow:

```text
1. User asks a task question.
2. MCP server calls memory.suggest_related.
3. System returns possible related memories.
4. Assistant shows suggestions.
5. User approves one or more memories.
6. MCP server calls memory.apply_context_bundle.
7. Assistant uses the returned instructions.
```

### Suggested UI Text

```text
I found related context that may help:

1. Minimal DAX fix style
   Confidence: 92%
   Reason: Matched DAX task type and Jira BI-482.

Apply this context?
[Apply] [Preview] [Ignore]
```

---

## 11. UI Requirements for POC

For MVP, UI can be minimal.

### Required UI Elements

- memory title
- confidence score
- short preview
- reason for match
- Apply button
- Preview button
- Ignore button

### Later UI Elements

- Edit memory
- Pin memory
- Mark stale
- Delete memory
- Convert to playbook
- Show source chats

---

## 12. Implementation Steps

### Step 1: Create Repository

Create the base monorepo structure.

Acceptance criteria:

- TypeScript MCP project exists
- Python memory engine project exists
- README includes setup commands
- `.env.example` exists

### Step 2: Build Python Memory Engine Skeleton

Create FastAPI app with health endpoint.

Endpoint:

```http
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

Acceptance criteria:

- API starts on port 8001
- health endpoint returns 200
- pytest health test passes

### Step 3: Add ChromaDB Persistent Client

Implement `chroma_store.py`.

Requirements:

- create persistent client
- create/get collection `cognitive_memories`
- support upsert
- support query

Acceptance criteria:

- memory can be inserted
- memory persists after restart
- query returns saved memory

### Step 4: Implement Memory Save API

Implement `POST /memory/save`.

Acceptance criteria:

- validates required fields
- creates deterministic or generated memory ID
- stores document in ChromaDB
- stores metadata
- returns memory ID

### Step 5: Implement Memory Search API

Implement `POST /memory/search`.

Acceptance criteria:

- accepts query
- returns top N results
- supports status filter
- supports type filter
- does not return rejected/archived by default

### Step 6: Implement Suggest Related API

Implement `POST /memory/suggest`.

Acceptance criteria:

- uses ChromaDB query
- applies ranking logic
- returns reason string
- returns confidence
- only returns results above threshold

### Step 7: Implement Context Bundle API

Implement `POST /context/bundle`.

Acceptance criteria:

- accepts approved memory IDs
- returns compact instruction list
- includes source memory IDs
- rejects rejected/archived memories

### Step 8: Build TypeScript MCP Server Skeleton

Acceptance criteria:

- MCP server starts
- registers at least one test tool
- can call Python `/health`

### Step 9: Add MCP Tool Schemas

Implement Zod schemas for:

- memory.save
- memory.search
- memory.suggest_related
- memory.apply_context_bundle
- profile.get

Acceptance criteria:

- invalid inputs fail clearly
- valid inputs call Python API

### Step 10: End-to-End Local Demo

Demo sequence:

1. Save DAX memory.
2. Search for similar DAX task.
3. Suggest related context.
4. Apply selected memory into context bundle.
5. Show assistant-ready instructions.

Acceptance criteria:

- demo can be executed using a script or manual commands
- all APIs return expected outputs
- context bundle is concise and usable

---

## 13. Validation Rules

### Memory Save Validation

Required:

- user_id
- workspace_id
- type
- title
- summary
- content
- scope
- status

Rules:

- title length <= 120
- summary length <= 500
- content length <= 5000 for POC
- tags max count = 20
- linked entities max count = 20
- status must be valid enum
- scope must be valid enum
- type must be valid enum

### Memory Search Validation

Rules:

- query length >= 3
- max_results between 1 and 20
- user_id and workspace_id required
- default filter should include status = approved

### Suggest Related Validation

Rules:

- current_query length >= 3
- max_results between 1 and 10
- linked_ids optional
- exclude rejected and archived by default
- return empty suggestions if score below threshold

### Context Bundle Validation

Rules:

- at least one memory ID required
- max 5 memory IDs for POC
- all memory IDs must belong to user/workspace
- all memory IDs must be approved
- instructions should be concise

---

## 14. Unit Test Plan — Python

### Test File: test_memory_save.py

Test cases:

1. saves valid memory
2. rejects missing title
3. rejects invalid memory type
4. rejects invalid status
5. stores metadata correctly
6. can retrieve saved memory by ID

### Test File: test_memory_search.py

Test cases:

1. returns relevant saved memory
2. respects max_results
3. filters by status approved
4. does not return rejected memory by default
5. returns empty result for unrelated query
6. handles empty database

### Test File: test_memory_suggest.py

Test cases:

1. suggests related DAX memory for DAX query
2. boosts linked Jira ID match
3. excludes low-score memory
4. includes confidence value
5. includes reason text
6. requires approval flag is true

### Test File: test_ranking.py

Test cases:

1. vector similarity dominates score
2. linked ID increases score
3. approved status increases score
4. rejected memory is excluded
5. old memory receives lower recency boost

### Test File: test_context_bundle.py

Test cases:

1. builds bundle from approved memory
2. rejects rejected memory
3. rejects archived memory
4. limits bundle to max memory count
5. includes source memory IDs
6. produces concise instructions

---

## 15. Unit Test Plan — TypeScript

### Test File: memoryEngineClient.test.ts

Test cases:

1. calls Python save endpoint
2. handles Python API errors
3. times out cleanly
4. maps response shape correctly
5. passes authorization/config headers if configured

### Test File: memorySave.test.ts

Test cases:

1. validates correct input
2. rejects missing user ID
3. rejects invalid memory type
4. forwards valid request to Python engine
5. returns memory ID

### Test File: memorySuggestRelated.test.ts

Test cases:

1. validates current query
2. defaults max_results to 3
3. calls `/memory/suggest`
4. returns suggestions
5. handles no suggestions

### Test File: memoryApplyContextBundle.test.ts

Test cases:

1. validates memory IDs
2. rejects empty memory ID list
3. calls `/context/bundle`
4. returns instruction bundle
5. handles rejected memory response

---

## 16. Integration Test Plan

### Integration Test 1: Save and Search

Steps:

1. Start Python engine.
2. Save memory through API.
3. Search similar query.
4. Verify saved memory appears.

Pass criteria:

- result includes saved memory ID
- score is above threshold

### Integration Test 2: MCP to Python

Steps:

1. Start Python engine.
2. Start TypeScript MCP server.
3. Invoke `memory.save` MCP tool.
4. Invoke `memory.suggest_related` MCP tool.

Pass criteria:

- MCP server returns valid suggestion
- no schema mismatch

### Integration Test 3: Full Context Bundle Flow

Steps:

1. Save approved DAX memory.
2. Ask similar DAX query.
3. Suggest related memory.
4. Apply memory.
5. Get context bundle.

Pass criteria:

- context bundle includes DAX-specific instruction
- bundle source includes original memory ID

---

## 17. Demo Script

### Demo 1: DAX Context Continuity

Save memory:

```text
Title: Minimal DAX fix style
Summary: User prefers minimal changes for DAX query fixes.
Content: Preserve existing measure names, do not rewrite full query, return corrected query first, then a short explanation.
Tags: dax, bi, minimal-change
Linked ID: BI-482
```

New user request:

```text
Can you fix this DAX measure using the previous BI-482 style?
```

Expected suggestion:

```text
Related context found: Minimal DAX fix style
Confidence: high
Reason: Matched DAX task type and BI-482.
```

Expected context bundle:

```text
- Make minimal DAX changes only.
- Preserve existing measure names.
- Return corrected DAX first.
- Keep explanation short.
```

### Demo 2: Communication Preference

Save memory:

```text
Title: User prefers answer first
Summary: User prefers direct answer before explanation.
Content: Start with the solution or code first, then provide explanation only if needed.
Tags: communication, response-format
```

New user request:

```text
Fix this script.
```

Expected bundle:

```text
- Provide the fixed script first.
- Keep explanation short and after the code.
```

### Demo 3: Rejected Pattern Avoidance

Save memory:

```text
Title: Avoid unnecessary refactor
Summary: User rejected previous responses that rewrote full modules unnecessarily.
Content: Do not refactor the full file unless explicitly requested. Prefer minimal patch.
Tags: rejected-pattern, coding-style
Status: approved
```

Expected behavior:

- Assistant avoids full rewrite.
- Assistant suggests minimal change approach.

---

## 18. Development Instructions for Codex or Antigravity

### General Agent Instructions

Use these instructions when asking an AI coding agent to build the project:

```text
You are building an MVP POC for Cognitive Continuity Layer for AI Assistants.

Build a monorepo with:
1. TypeScript MCP server in `mcp-server-ts`
2. Python FastAPI memory engine in `memory-engine-py`
3. ChromaDB persistent vector storage
4. Unit tests for both TypeScript and Python
5. A local demo script showing save → suggest → apply context bundle

Follow the architecture and schemas in this document.
Do not add unnecessary enterprise features yet.
Prioritize correctness, testability, and clear contracts between TypeScript and Python.
```

### Recommended Agent Work Breakdown

Use small tasks rather than one large prompt.

#### Task 1: Scaffold repository

```text
Create the monorepo structure for the project. Add README, .env.example, TypeScript MCP server folder, Python memory engine folder, and docs folder. Do not implement business logic yet.
```

#### Task 2: Build Python health API

```text
Implement FastAPI app with GET /health. Add pytest test for health endpoint. Add requirements.txt.
```

#### Task 3: Add ChromaDB store

```text
Implement ChromaDB persistent client in memory-engine-py/app/chroma_store.py. Create or get collection cognitive_memories. Add functions upsert_memory and query_memories. Add tests using temporary Chroma directory.
```

#### Task 4: Add Python schemas

```text
Create Pydantic schemas for MemorySaveRequest, MemorySearchRequest, MemorySuggestRequest, ContextBundleRequest, and their response models. Add validation rules from the context document.
```

#### Task 5: Implement save/search/suggest/bundle APIs

```text
Implement /memory/save, /memory/search, /memory/suggest, and /context/bundle. Use ChromaDB for storage and retrieval. Implement basic ranking logic. Add pytest coverage.
```

#### Task 6: Scaffold TypeScript MCP server

```text
Create TypeScript MCP server using @modelcontextprotocol/sdk. Add config handling and memoryEngineClient. Register tools but use mocked responses first.
```

#### Task 7: Connect MCP tools to Python engine

```text
Wire memory.save, memory.search, memory.suggest_related, memory.apply_context_bundle, and profile.get to the Python FastAPI endpoints. Use Zod validation. Add Vitest unit tests.
```

#### Task 8: Build end-to-end demo

```text
Create demo script or documented curl commands showing: save memory, suggest related memory, apply context bundle. Use the DAX BI-482 scenario.
```

#### Task 9: Add validation and hardening

```text
Review all validation rules. Add error handling for invalid input, unavailable Python engine, empty ChromaDB, and low-score suggestions.
```

### Agent Safety Instructions

```text
Do not delete files outside this repository.
Do not run destructive commands.
Do not install global packages.
Do not call external APIs unless explicitly configured.
Do not store raw secrets in code.
Do not silently change architecture without updating docs.
For any generated code, include tests.
```

---

## 19. Acceptance Criteria for MVP POC

The MVP is successful when:

1. Python memory engine starts locally.
2. ChromaDB persists saved memories.
3. TypeScript MCP server starts locally.
4. MCP tools call Python endpoints successfully.
5. A memory can be saved with tags and linked IDs.
6. Similar memory can be retrieved from a new query.
7. Related context suggestion includes confidence and reason.
8. Context is not applied silently.
9. Context bundle is generated only after selection.
10. Unit tests pass for Python and TypeScript.
11. Demo scenario works end to end.

---

## 20. Non-Goals for MVP

Do not build these in the first POC:

- full enterprise RBAC
- SSO
- admin dashboard
- automatic raw chat ingestion
- multi-tenant production deployment
- complex knowledge graph
- automatic memory learning without approval
- browser extension
- full UI app
- cloud deployment pipeline

These can be planned after the POC proves value.

---

## 21. Future Enhancements

After MVP:

- automatic memory extraction from accepted conversations
- UI cards using MCP Apps or host-specific UI
- team-shared memory
- memory expiry and review workflow
- Jira/Git integration
- audit logs
- privacy controls
- advanced reranking
- knowledge graph
- analytics dashboard
- support for multiple assistants
- context portability across IDEs and chat tools

---

## 22. Success Metrics

For POC, measure:

```text
- number of saved memories
- number of successful context suggestions
- suggestion acceptance rate
- repeated explanation reduction
- average prompt length reduction
- user-rated usefulness
- number of avoided re-explanations
```

Qualitative success:

```text
The user should feel that the assistant remembers how they work without needing to repeat instructions in every new chat.
```

---

## 23. Final MVP Principle

Start simple:

```text
Manual save + smart retrieval + user approval
```

Avoid over-automation in the first version.

The differentiator is not just storing memory. The differentiator is safe, explainable, user-approved continuity across AI assistant interactions.

