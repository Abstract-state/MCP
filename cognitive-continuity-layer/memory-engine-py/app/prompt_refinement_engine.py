from typing import List, Dict, Any
from app.behavioral_retriever import BehavioralRetriever
from app.signal_extractor import SignalExtractor

class PromptRefinementEngine:
    def __init__(self, retriever: BehavioralRetriever):
        self.retriever = retriever
        self.signal_extractor = SignalExtractor()

    def generate_preview(self, query: str, user_id: str, workspace_id: str, linked_ids: List[str] = None) -> Dict[str, Any]:
        # 1. Signal Extraction
        signals = self.signal_extractor.extract_signals(query)
        
        # 2. Behavioral Retrieval
        candidates = self.retriever.retrieve(query=query, user_id=user_id, workspace_id=workspace_id, limit=3)
        
        # 3. Interpret Meaning
        interpreted_meaning = []
        retrieved_context = []
        
        if signals.get('task_type') != "unknown":
            interpreted_meaning.append(f"Task intent appears to be: {signals['task_type']}")
            
        for phrase in signals.get('behavior_phrases', []):
            interpreted_meaning.append(f"Detected behavioral instruction: '{phrase}'")
            
        for c in candidates:
            # We use the document or summary for context
            doc = c.get('document', '')
            if doc:
                retrieved_context.append(doc[:100] + "...")
                
        if not interpreted_meaning:
            interpreted_meaning.append("Direct execution requested without implicit behavioral instructions.")
            
        # 4. Refinement Proposal Synthesis
        refined_prompt = query
        if retrieved_context:
            refined_prompt += "\n\n# Context Applied:\n- " + "\n- ".join(retrieved_context)
            
        return {
            "interpreted_meaning": interpreted_meaning,
            "retrieved_context": retrieved_context,
            "refined_prompt": refined_prompt
        }
