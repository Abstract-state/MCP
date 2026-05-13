import uuid
import json
from app.chroma_store import ChromaStore
from app.schemas import (
    EpisodeCaptureRequest, EpisodeCaptureResponse,
    EpisodeAnalyzeRequest, EpisodeAnalyzeResponse,
    PromptRefinePreviewRequest, PromptRefinePreviewResponse, RefinementProposal,
    PromptRefineConfirmRequest, PromptRefineConfirmResponse,
    ConversationEpisode
)
from app.episode_analyzer import EpisodeAnalyzer
from app.behavioral_retriever import BehavioralRetriever
from app.prompt_refinement_engine import PromptRefinementEngine

class BehavioralService:
    def __init__(self, store: ChromaStore):
        self.store = store
        self.episode_analyzer = EpisodeAnalyzer()
        self.retriever = BehavioralRetriever(store)
        self.refinement_engine = PromptRefinementEngine(self.retriever)

    def capture_episode_turn(self, req: EpisodeCaptureRequest) -> EpisodeCaptureResponse:
        # For POC, we'll try to fetch the existing episode from Chroma
        doc = self.store.get_memory_by_id(req.episode_id, collection_name="conversation_episodes")
        
        if doc:
            metadata = doc['metadata']
            episode = ConversationEpisode.parse_raw(metadata['episode_json'])
            episode.turns.append(req.turn)
        else:
            # Create a new one
            episode = ConversationEpisode(
                episode_id=req.episode_id,
                workspace_id=req.workspace_id,
                user_id=req.user_id,
                assistant_client=req.assistant_client,
                model_used=req.model_used,
                initial_prompt=req.turn.message,
                turns=[req.turn]
            )

        # Upsert back
        self.store.upsert_memory(
            memory_id=req.episode_id,
            document=episode.initial_prompt + "\n" + "\n".join([t.message for t in episode.turns]),
            metadata={"user_id": req.user_id, "workspace_id": req.workspace_id, "episode_json": episode.json(), "accepted": episode.accepted},
            collection_name="conversation_episodes"
        )
        
        return EpisodeCaptureResponse(status="captured", episode_id=req.episode_id)

    def analyze_episode(self, req: EpisodeAnalyzeRequest) -> EpisodeAnalyzeResponse:
        doc = self.store.get_memory_by_id(req.episode_id, collection_name="conversation_episodes")
        if not doc:
            raise ValueError("Episode not found")
            
        metadata = doc['metadata']
        episode = ConversationEpisode.parse_raw(metadata['episode_json'])
        
        analyzed_episode = self.episode_analyzer.analyze(episode)
        
        # Save back the analyzed state
        self.store.upsert_memory(
            memory_id=req.episode_id,
            document=analyzed_episode.initial_prompt,
            metadata={
                "user_id": req.user_id, 
                "workspace_id": req.workspace_id, 
                "episode_json": analyzed_episode.json(), 
                "accepted": analyzed_episode.accepted
            },
            collection_name="conversation_episodes"
        )
        
        # For POC, assume 1 pattern/rule if accepted
        patterns = 1 if analyzed_episode.accepted else 0
        rules = 1 if analyzed_episode.accepted else 0
        
        return EpisodeAnalyzeResponse(
            episode_id=req.episode_id,
            friction_score=analyzed_episode.metrics.friction_score,
            accepted=analyzed_episode.accepted,
            patterns_extracted=patterns,
            rules_extracted=rules
        )

    def refine_preview(self, req: PromptRefinePreviewRequest) -> PromptRefinePreviewResponse:
        preview = self.refinement_engine.generate_preview(
            query=req.prompt,
            user_id=req.user_id,
            workspace_id=req.workspace_id,
            linked_ids=req.linked_ids
        )
        
        return PromptRefinePreviewResponse(
            original_prompt=req.prompt,
            proposal=RefinementProposal(**preview)
        )

    def refine_confirm(self, req: PromptRefineConfirmRequest) -> PromptRefineConfirmResponse:
        if not req.accepted:
            return PromptRefineConfirmResponse(status="rejected")
            
        # Optional: Save the confirmed prompt rule back into prompt_refinement_rules
        rule_id = str(uuid.uuid4())
        self.store.upsert_memory(
            memory_id=rule_id,
            document=req.original_prompt,
            metadata={
                "user_id": req.user_id, 
                "workspace_id": req.workspace_id, 
                "refined_prompt": req.approved_prompt
            },
            collection_name="prompt_refinement_rules"
        )
        
        return PromptRefineConfirmResponse(status="confirmed")
