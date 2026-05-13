from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

# -----------------
# ENUMS
# -----------------

class MemoryType(str, Enum):
    preference = "preference"
    communication_pattern = "communication_pattern"
    task_context = "task_context"
    accepted_pattern = "accepted_pattern"
    rejected_pattern = "rejected_pattern"
    playbook = "playbook"
    constraint = "constraint"
    decision = "decision"

class MemoryStatus(str, Enum):
    draft = "draft"
    suggested = "suggested"
    approved = "approved"
    rejected = "rejected"
    archived = "archived"

class MemoryScope(str, Enum):
    private = "private"
    project = "project"
    workspace = "workspace"
    team = "team"
    organization = "organization"

class LinkedEntity(BaseModel):
    type: str
    id: str

# -----------------
# REQUEST MODELS
# -----------------

class MemorySaveRequest(BaseModel):
    user_id: str
    workspace_id: str
    type: MemoryType
    title: str = Field(..., max_length=120)
    summary: str = Field(..., max_length=500)
    content: str = Field(..., max_length=5000)
    tags: Optional[List[str]] = Field(default=[], max_length=20)
    linked_entities: Optional[List[LinkedEntity]] = Field(default=[], max_length=20)
    scope: MemoryScope
    status: MemoryStatus

class MemorySearchFilters(BaseModel):
    status: Optional[str] = "approved"
    type: Optional[str] = None

class MemorySearchRequest(BaseModel):
    user_id: str
    workspace_id: str
    query: str = Field(..., min_length=3)
    max_results: int = Field(default=5, ge=1, le=20)
    filters: Optional[MemorySearchFilters] = Field(default_factory=MemorySearchFilters)

class MemorySuggestRequest(BaseModel):
    user_id: str
    workspace_id: str
    current_query: str = Field(..., min_length=3)
    linked_ids: Optional[List[str]] = Field(default=[])
    max_results: int = Field(default=3, ge=1, le=10)

class ContextBundleRequest(BaseModel):
    user_id: str
    workspace_id: str
    memory_ids: List[str] = Field(..., min_length=1, max_length=5)

class ProfileGetRequest(BaseModel):
    user_id: str
    workspace_id: str

# -----------------
# RESPONSE MODELS
# -----------------

class MemorySaveResponse(BaseModel):
    memory_id: str
    status: str

class SearchResultMetadata(BaseModel):
    type: str
    status: str
    linked_ids: Optional[str] = None

class SearchResultItem(BaseModel):
    memory_id: str
    title: str
    summary: str
    score: float
    metadata: SearchResultMetadata

class MemorySearchResponse(BaseModel):
    results: List[SearchResultItem]

class SuggestionItem(BaseModel):
    memory_id: str
    title: str
    reason: str
    confidence: float
    preview: str
    requires_approval: bool

class MemorySuggestResponse(BaseModel):
    suggestions: List[SuggestionItem]
    message: Optional[str] = None

class ContextBundle(BaseModel):
    bundle_id: str
    instructions: List[str]
    source_memory_ids: List[str]

class ContextBundleResponse(BaseModel):
    context_bundle: ContextBundle

class Profile(BaseModel):
    user_id: str
    preferences: List[str]

class ProfileGetResponse(BaseModel):
    profile: Profile

# -----------------
# BEHAVIORAL MODELS
# -----------------

class ConversationTurn(BaseModel):
    turn_id: str
    role: str
    message: str
    turn_type: Optional[str] = None # 'correction', 'clarification', etc.

class FrictionMetrics(BaseModel):
    turn_count: int = 0
    clarification_count: int = 0
    correction_count: int = 0
    rejection_count: int = 0
    friction_score: float = 0.0

class ConversationEpisode(BaseModel):
    episode_id: str
    workspace_id: str
    user_id: str
    assistant_client: Optional[str] = None
    model_used: Optional[str] = None
    initial_prompt: str
    final_understood_intent: Optional[str] = None
    turns: List[ConversationTurn] = []
    metrics: FrictionMetrics = Field(default_factory=FrictionMetrics)
    accepted: bool = False
    acceptance_signal: Optional[str] = None
    linked_ids: List[str] = []

class CommunicationPattern(BaseModel):
    pattern: str
    meaning: List[str]
    confidence: float
    usage_count: int = 1

class PromptRefinementRule(BaseModel):
    trigger_phrase: str
    context: str
    refinement: List[str]

# -----------------
# BEHAVIORAL REQUEST/RESPONSE MODELS
# -----------------

class EpisodeCaptureRequest(BaseModel):
    user_id: str
    workspace_id: str
    episode_id: str
    turn: ConversationTurn
    assistant_client: Optional[str] = None
    model_used: Optional[str] = None

class EpisodeCaptureResponse(BaseModel):
    status: str
    episode_id: str

class EpisodeAnalyzeRequest(BaseModel):
    user_id: str
    workspace_id: str
    episode_id: str

class EpisodeAnalyzeResponse(BaseModel):
    episode_id: str
    friction_score: float
    accepted: bool
    patterns_extracted: int
    rules_extracted: int

class PromptRefinePreviewRequest(BaseModel):
    user_id: str
    workspace_id: str
    prompt: str
    linked_ids: Optional[List[str]] = []

class RefinementProposal(BaseModel):
    interpreted_meaning: List[str]
    retrieved_context: List[str]
    refined_prompt: str

class PromptRefinePreviewResponse(BaseModel):
    original_prompt: str
    proposal: RefinementProposal

class PromptRefineConfirmRequest(BaseModel):
    user_id: str
    workspace_id: str
    original_prompt: str
    approved_prompt: str
    accepted: bool

class PromptRefineConfirmResponse(BaseModel):
    status: str

