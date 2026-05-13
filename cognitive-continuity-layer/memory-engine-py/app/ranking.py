from datetime import datetime, timezone

def calculate_score(distance: float, metadata: dict, requested_linked_ids: list[str]) -> float:
    # 1. Vector similarity: using 1.0 / (1.0 + distance) as proxy for cosine similarity
    vector_similarity = 1.0 / (1.0 + distance)
    
    # 2. Linked ID match
    linked_id_match = 0.0
    mem_linked_ids = metadata.get("linked_ids", "")
    if mem_linked_ids and requested_linked_ids:
        mem_ids = [v.strip() for v in mem_linked_ids.split(",") if v.strip()]
        if any(req_id in mem_ids for req_id in requested_linked_ids):
            linked_id_match = 1.0
            
    # 3. Status boost
    status = metadata.get("status", "")
    approved_status_boost = 0.0
    if status == "approved":
        approved_status_boost = 1.0
    elif status == "suggested":
        approved_status_boost = 0.2
        
    # 4. Recency boost
    recency_boost = 0.0
    updated_at_str = metadata.get("updated_at")
    if updated_at_str:
        try:
            # Handle standard ISO formats, even with Z
            updated_at_str = updated_at_str.replace("Z", "+00:00")
            updated_at = datetime.fromisoformat(updated_at_str)
            now = datetime.now(timezone.utc)
            delta_days = (now - updated_at).days
            if delta_days <= 7:
                recency_boost = 1.0
            elif delta_days <= 30:
                recency_boost = 0.6
        except Exception:
            pass
            
    final_score = (
        0.70 * vector_similarity +
        0.15 * linked_id_match +
        0.10 * approved_status_boost +
        0.05 * recency_boost
    )
    
    return final_score
