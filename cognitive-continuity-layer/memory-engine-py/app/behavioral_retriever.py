from typing import List, Dict, Any
from app.chroma_store import ChromaStore
from app.hybrid_ranker import HybridRanker

class BehavioralRetriever:
    def __init__(self, store: ChromaStore):
        self.store = store
        self.ranker = HybridRanker()
        self.collections_to_search = [
            "cognitive_memories",
            "conversation_episodes",
            "prompt_refinement_rules",
            "accepted_task_contexts"
        ]

    def retrieve(self, query: str, user_id: str, workspace_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        where_filter = {
            "$and": [
                {"user_id": user_id},
                {"workspace_id": workspace_id}
            ]
        }
        
        candidates = []
        
        for coll_name in self.collections_to_search:
            try:
                results = self.store.query_memories(
                    query_texts=[query],
                    n_results=limit,
                    where=where_filter,
                    collection_name=coll_name
                )
                
                if results and results['ids'] and len(results['ids']) > 0:
                    for i in range(len(results['ids'][0])):
                        candidates.append({
                            'id': results['ids'][0][i],
                            'document': results['documents'][0][i],
                            'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                            'distance': results['distances'][0][i] if 'distances' in results and results['distances'] else 1.0,
                            'collection': coll_name
                        })
            except Exception as e:
                # Collection might not exist yet or be empty
                pass
                
        # Deduplicate by ID just in case
        seen = set()
        unique_candidates = []
        for c in candidates:
            if c['id'] not in seen:
                seen.add(c['id'])
                unique_candidates.append(c)
                
        # Rank the candidates
        ranked = self.ranker.rank(unique_candidates, query)
        
        # Return top N
        return ranked[:limit]
