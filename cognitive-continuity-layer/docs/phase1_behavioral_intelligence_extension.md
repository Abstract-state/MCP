# Phase 1 Behavioral Intelligence Extension
# Cognitive Continuity Layer for AI Assistants

---

# 1. Purpose

This document extends the base MVP architecture defined in:

docs/cognitive_continuity_mvp_poc_context.md

The original MVP focused on:

- reusable memory
- cross-chat continuity
- MCP integration
- ChromaDB persistence
- reusable task context

This extension introduces:

- behavioral learning
- communication interpretation
- friction-aware learning
- episodic retrieval
- hybrid behavioral retrieval
- prompt refinement intelligence
- acceptance-aware reinforcement
- human-approved prompt enhancement

This extension defines the TRUE Phase 1 architecture.

---

# 2. Core Problem Statement

Modern AI assistants fail frequently because:

1. The assistant does not understand what the user actually means.
2. User communication styles differ significantly.
3. Context is lost across chat instances.
4. Users repeatedly re-explain the same expectations.
5. Successful prompt patterns are not reused.
6. AI assistants do not learn from clarification journeys.

The goal is NOT merely memory storage.

The goal is:

- learning how the user communicates
- learning what successful outcomes looked like
- learning how confusion was resolved
- reducing future clarification cycles
- improving prompt interpretation quality

---

# 3. Phase 1 Core Goals

Phase 1 focuses on TWO capabilities.

---

## Goal 1 — Communication Learning

Learn how the user communicates and what they actually mean.

Example:

User phrase:

"minimal changes"

Actual meaning:

- avoid refactor
- preserve structure
- keep diff small

The system should learn this from accepted outcomes and repeated correction patterns.

---

## Goal 2 — Cross-Chat Context Continuity

Reuse successful context across independent chat sessions.

Examples:

- DAX formatting approach
- accepted coding constraints
- Jira-linked implementation style
- debugging preferences
- architectural constraints
- previously accepted workflow context

The system should retrieve these and propose prompt refinements.

---

# 4. IMPORTANT SAFETY PRINCIPLE

The system must NEVER silently modify prompts.

The system must:

1. generate a proposed refined prompt
2. show the proposal to the user
3. require explicit approval
4. only then send the refined prompt to the LLM

Correct flow:

User Prompt
    ↓
Behavioral Retrieval
    ↓
Prompt Refinement Proposal
    ↓
User Approval
    ↓
LLM Execution

---

# 5. Architectural Evolution

This system is NOT traditional RAG.

Traditional RAG retrieves:

- markdown
- documentation
- code snippets
- repo knowledge

This system retrieves:

- communication meanings
- accepted behavioral patterns
- successful episodes
- reusable constraints
- refinement rules
- accepted workflow context

This architecture becomes:

# Behavioral Episodic Retrieval System

---

# 6. High-Level Behavioral Architecture

User Prompt
    ↓
Prompt Intake Layer
    ↓
Signal Extraction
    ↓
Behavioral Retrieval Engine
    ↓
Hybrid Ranking Engine
    ↓
Prompt Refinement Generator
    ↓
Refinement Proposal
    ↓
User Approval
    ↓
Final Prompt Sent To LLM

---

# 7. Core Architectural Components

## A. Prompt Intake Layer

Responsible for:

- receiving raw prompts
- collecting model/client metadata
- collecting workspace/user metadata
- preparing signals for retrieval

---

## B. Signal Extraction Layer

Extracts:

- entities
- continuity phrases
- behavior phrases
- linked IDs
- task types
- correction signals
- clarification signals

Example:

Input:

"Fix this DAX query same as before with minimal changes"

Extracted:

{
  "entities": ["DAX"],
  "behavior_phrases": [
    "same as before",
    "minimal changes"
  ],
  "task_type": "query_fix"
}

---

## C. Behavioral Retrieval Engine

Performs:

- semantic retrieval
- sparse retrieval
- episodic retrieval
- communication-pattern retrieval
- accepted-context retrieval

This is the core intelligence layer.

---

## D. Hybrid Ranking Engine

Combines multiple scoring signals.

This engine should NOT rely only on cosine similarity.

---

## E. Prompt Refinement Generator

Builds:

- interpreted constraints
- reusable accepted context
- prompt refinement proposal

The original prompt must always remain visible.

---

## F. Approval Layer

The user must approve refinement before LLM execution.

No hidden prompt mutation is allowed.

---

# 8. Conversation Episode Architecture

A complete conversation session becomes an episode.

The system should learn from:

- the original prompt
- clarification turns
- correction turns
- final accepted interpretation
- accepted outcomes
- rejection patterns
- friction metrics
- assistant/model used

---

# 9. Conversation Episode Object

{
  "episode_id": "ep_001",
  "workspace_id": "corp_ws",
  "user_id": "demo_user",

  "assistant_client": "copilot",
  "model_used": "gemini-pro",

  "initial_prompt": "Fix this query same as before",

  "final_understood_intent":
    "Fix DAX query using previously accepted BI-482 formatting style",

  "turn_count": 8,
  "clarification_count": 3,
  "correction_count": 2,
  "rejection_count": 1,

  "accepted": true,
  "acceptance_signal": "user_message_ok",

  "linked_ids": ["BI-482"],

  "friction_score": 7.5
}

---

# 10. Conversation Turn Object

{
  "turn_id": "turn_001",
  "episode_id": "ep_001",
  "role": "user",
  "message": "No, preserve existing measure names",
  "turn_type": "correction"
}

---

# 11. Acceptance Signals

The system must learn from accepted outcomes.

Accepted signals include:

- ok
- accepted
- works
- this works
- thank you
- thanks
- looks good
- perfect

Rejected signals include:

- no
- wrong
- incorrect
- not this
- not what I meant
- this broke
- don't do this

Clarification signals include:

- I meant
- actually
- not like this
- same as before
- minimal changes

---

# 12. Friction Learning

The system must measure how difficult it was for the LLM to understand the user.

This becomes:

# Friction Score

Formula:

friction_score =
(clarification_count * 2)
+ (correction_count * 3)
+ (rejection_count * 4)
+ (turn_count * 0.5)
- acceptance_bonus

Purpose:

High-friction accepted episodes are valuable learning opportunities.

They reveal what the user ACTUALLY meant.

---

# 13. Communication Pattern Learning

The system should learn repeated communication meanings.

Example:

"minimal changes"

maps to:

- avoid major refactor
- preserve structure
- small diff preferred

---

# 14. Communication Pattern Object

{
  "pattern": "minimal changes",
  "meaning": [
    "avoid major refactor",
    "preserve structure",
    "small diff preferred"
  ],
  "confidence": 0.91,
  "usage_count": 14
}

---

# 15. Prompt Refinement Rules

Prompt refinement rules are reusable interpretation rules.

Example:

{
  "trigger_phrase": "same as before",
  "context": "DAX",
  "refinement": [
    "reuse previously accepted DAX formatting style",
    "preserve measure names",
    "return corrected query first"
  ]
}

---

# 16. Retrieval Architecture

DO NOT rely only on cosine similarity.

The system must use:

# Multi-Stage Hybrid Behavioral Retrieval

---

# 17. Retrieval Pipeline

## Stage 1 — Signal Extraction

Extract:

- entities
- linked IDs
- continuity phrases
- behavior phrases
- task type
- model/client context

---

## Stage 2 — Multi-Strategy Retrieval

Perform:

- semantic retrieval
- sparse retrieval
- episodic retrieval
- communication retrieval
- accepted-context retrieval

---

## Stage 3 — Hybrid Reranking

Apply weighted reranking.

---

## Stage 4 — Refinement Generation

Generate refinement proposal.

---

## Stage 5 — User Approval

Require explicit approval before use.

---

# 18. Retrieval Types

## A. Semantic Retrieval

Purpose:

Retrieve semantically related context.

Recommended embeddings:

- bge-small-en-v1.5
- e5-small-v2
- gte-small

---

## B. Sparse Retrieval

Purpose:

Retrieve exact phrases and keywords.

Recommended library:

rank-bm25

---

## C. Episodic Retrieval

Purpose:

Retrieve similar successful conversation journeys.

This is more valuable than document retrieval.

Examples:

- similar corrections
- similar clarification journeys
- similar accepted outcomes

---

## D. Constraint Retrieval

Purpose:

Retrieve reusable accepted constraints.

Examples:

- avoid refactor
- preserve structure
- compact formatting

---

## E. Communication Pattern Retrieval

Purpose:

Interpret user-specific phrasing.

Examples:

- same as before
- minimal changes
- quick fix

---

# 19. Hybrid Ranking Formula

The system must use weighted hybrid retrieval.

NOT vector similarity only.

Recommended formula:

final_score =
0.30 dense_embedding_similarity
+ 0.20 BM25_keyword_score
+ 0.20 episodic_similarity
+ 0.10 accepted_outcome_score
+ 0.10 friction_reduction_score
+ 0.05 recency_score
+ 0.05 model_success_rate

---

# 20. Episodic Similarity

The system should retrieve:

- previous successful episodes
- accepted correction journeys
- similar clarification patterns
- accepted final meanings

This is a key architectural differentiator.

---

# 21. Acceptance-Based Reinforcement

Accepted outcomes should reinforce learning.

Rejected outcomes should reduce confidence.

Example:

new_confidence =
accepted_count / total_count

---

# 22. Prompt Refinement Pipeline

The system should NEVER silently mutate prompts.

Pipeline:

Raw User Prompt
    ↓
Behavioral Retrieval
    ↓
Refinement Proposal
    ↓
User Review
    ↓
User Approval
    ↓
Final Prompt To LLM

---

# 23. Example Prompt Refinement

User Prompt:

"Fix this DAX query same as before with minimal changes"

Generated Proposal:

Communication Interpretation:
- avoid major refactor
- preserve existing structure

Relevant Prior Context:
- preserve DAX measure names
- compact formatting
- return corrected query first

Original User Request:
Fix this DAX query same as before with minimal changes

---

# 24. Required Collections

The system should maintain separate collections.

---

## Collection 1 — conversation_episodes

Stores:

- episodes
- friction metrics
- accepted outcomes

---

## Collection 2 — communication_patterns

Stores:

- phrase → meaning mappings

---

## Collection 3 — prompt_refinement_rules

Stores:

- reusable refinement rules

---

## Collection 4 — accepted_task_contexts

Stores:

- reusable successful context

---

# 25. Required Python Modules

episode_analyzer.py
acceptance_detector.py
friction_calculator.py
prompt_refinement_engine.py
behavioral_retriever.py
hybrid_ranker.py
signal_extractor.py

---

# 26. Required APIs

POST /episode/capture
POST /episode/analyze

POST /communication/learn
POST /communication/search

POST /prompt/refine-preview
POST /prompt/refine-confirm

---

# 27. Required MCP Tools

episode.capture
episode.analyze

communication.learn
communication.search

prompt.refine_preview
prompt.refine_confirm

feedback.capture

---

# 28. Storage Rules

IMPORTANT:

Do NOT store full raw chats by default.

Store:

- distilled episodes
- learned patterns
- refinement rules
- accepted context summaries

Only store raw chats if explicitly enabled.

---

# 29. Enterprise Design Principles

The system must:

- require user approval
- avoid hidden prompt mutation
- support workspace isolation
- support future enterprise auth integration
- avoid unnecessary sensitive data retention

---

# 30. Current Phase Boundaries

Phase 1 includes:

- behavioral learning
- friction learning
- episodic retrieval
- prompt refinement preview
- user confirmation
- cross-chat continuity

Phase 1 does NOT include:

- dashboards
- advanced UI
- autonomous agents
- predictive automation
- organization-wide graph intelligence

---

# 31. Final Product Definition

Phase 1 delivers:

Behavioral Prompt Intelligence
+
Cross-Chat Continuity
+
Human-Approved Prompt Refinement

The system learns:

- how the user communicates
- what the user actually means
- which contexts were successful
- how confusion was resolved
- how to improve future prompt interpretation