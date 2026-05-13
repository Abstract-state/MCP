from fastapi import FastAPI, Depends
from app.schemas import MemorySaveRequest, MemorySaveResponse, MemorySearchRequest, MemorySearchResponse
from app.schemas import MemorySuggestRequest, MemorySuggestResponse, ContextBundleRequest, ContextBundleResponse
from app.schemas import EpisodeCaptureRequest, EpisodeCaptureResponse, EpisodeAnalyzeRequest, EpisodeAnalyzeResponse
from app.schemas import PromptRefinePreviewRequest, PromptRefinePreviewResponse, PromptRefineConfirmRequest, PromptRefineConfirmResponse
from app.chroma_store import ChromaStore
from app.memory_service import MemoryService
from app.behavioral_service import BehavioralService

app = FastAPI(title="Cognitive Continuity Memory Engine")

# Global store instance (for POC, single instance is fine)
store = ChromaStore()
memory_service = MemoryService(store=store)
behavioral_service = BehavioralService(store=store)

def get_memory_service() -> MemoryService:
    return memory_service

def get_behavioral_service() -> BehavioralService:
    return behavioral_service

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/memory/save", response_model=MemorySaveResponse)
def save_memory(request: MemorySaveRequest, service: MemoryService = Depends(get_memory_service)):
    return service.save_memory(request)

@app.post("/memory/search", response_model=MemorySearchResponse)
def search_memory(request: MemorySearchRequest, service: MemoryService = Depends(get_memory_service)):
    return service.search_memory(request)

@app.post("/memory/suggest", response_model=MemorySuggestResponse)
def suggest_related(request: MemorySuggestRequest, service: MemoryService = Depends(get_memory_service)):
    return service.suggest_related(request)

@app.post("/context/bundle", response_model=ContextBundleResponse)
def context_bundle(request: ContextBundleRequest, service: MemoryService = Depends(get_memory_service)):
    return service.context_bundle(request)

@app.post("/episode/capture", response_model=EpisodeCaptureResponse)
def capture_episode(request: EpisodeCaptureRequest, service: BehavioralService = Depends(get_behavioral_service)):
    return service.capture_episode_turn(request)

@app.post("/episode/analyze", response_model=EpisodeAnalyzeResponse)
def analyze_episode(request: EpisodeAnalyzeRequest, service: BehavioralService = Depends(get_behavioral_service)):
    return service.analyze_episode(request)

@app.post("/prompt/refine-preview", response_model=PromptRefinePreviewResponse)
def refine_preview(request: PromptRefinePreviewRequest, service: BehavioralService = Depends(get_behavioral_service)):
    return service.refine_preview(request)

@app.post("/prompt/refine-confirm", response_model=PromptRefineConfirmResponse)
def refine_confirm(request: PromptRefineConfirmRequest, service: BehavioralService = Depends(get_behavioral_service)):
    return service.refine_confirm(request)

