import re
from typing import List, Dict, Any

class SignalExtractor:
    def __init__(self):
        self.continuity_phrases = [
            "same as before", "minimal changes", "like last time", "as usual"
        ]
        
    def extract_signals(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        # Extract JIRA/Ticket IDs (e.g., PROJ-123)
        linked_ids = re.findall(r'[A-Z]+-\d+', text)
        
        # Extract behavior phrases
        behavior_phrases = [
            phrase for phrase in self.continuity_phrases 
            if phrase in text_lower
        ]
        
        # Infer task type naively
        task_type = "unknown"
        if "fix" in text_lower or "debug" in text_lower:
            task_type = "fix"
        elif "refactor" in text_lower or "clean" in text_lower:
            task_type = "refactor"
        elif "dax" in text_lower or "query" in text_lower:
            task_type = "query"
            
        return {
            "entities": [],
            "behavior_phrases": behavior_phrases,
            "task_type": task_type,
            "linked_ids": list(set(linked_ids))
        }
