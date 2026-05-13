from typing import List, Dict, Any

class HybridRanker:
    def rank(self, candidates: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        # A simple hybrid ranker without rank-bm25.
        # It relies on ChromaDB distances (converted to similarity)
        # and basic keyword overlap for pseudo-BM25.
        
        query_terms = set(query.lower().split())
        
        for candidate in candidates:
            # 1. Dense Embedding Similarity (from Chroma L2 distance)
            distance = candidate.get('distance', 1.0)
            dense_sim = 1.0 / (1.0 + distance)
            
            # 2. Pseudo-BM25 (Keyword overlap)
            content = candidate.get('document', '').lower()
            content_terms = set(content.split())
            overlap = len(query_terms.intersection(content_terms))
            bm25_score = min(1.0, overlap / max(1, len(query_terms)))
            
            # 3. Episodic Similarity
            episodic_score = 1.0 if candidate.get('collection') == 'conversation_episodes' else 0.0
            
            # 4. Accepted Outcome Score
            metadata = candidate.get('metadata', {})
            accepted_score = 1.0 if metadata.get('accepted', False) or metadata.get('status') == 'approved' else 0.0
            
            # 5. Friction Reduction Score (higher is better if we learned from high friction, but for ranking, we prioritize low friction or high friction learned rules)
            # We'll assign a flat bonus if it's an approved rule or episode
            friction_score = 0.5
            
            # 6. Recency (simplified flat for POC)
            recency_score = 1.0 
            
            # 7. Model Success Rate
            model_success = 1.0
            
            # Weighted Formula
            final_score = (
                (0.30 * dense_sim) +
                (0.20 * bm25_score) +
                (0.20 * episodic_score) +
                (0.10 * accepted_score) +
                (0.10 * friction_score) +
                (0.05 * recency_score) +
                (0.05 * model_success)
            )
            
            candidate['final_score'] = final_score
            
        # Sort descending by final_score
        return sorted(candidates, key=lambda x: x['final_score'], reverse=True)
