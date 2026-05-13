from datetime import datetime, timezone
import uuid
from typing import Dict, Any
from fastapi import HTTPException

from app.schemas import MemorySaveRequest, MemorySaveResponse, MemorySearchRequest, MemorySearchResponse, SearchResultItem, SearchResultMetadata
from app.schemas import MemorySuggestRequest, MemorySuggestResponse, SuggestionItem, ContextBundleRequest, ContextBundleResponse, ContextBundle
from app.chroma_store import ChromaStore
from app.ranking import calculate_score

class MemoryService:
    def __init__(self, store: ChromaStore):
        self.store = store

    def save_memory(self, request: MemorySaveRequest) -> MemorySaveResponse:
        memory_id = f"mem_{uuid.uuid4().hex}"
        
        # Format tags and linked_entities to comma separated strings
        tags_str = ",".join(request.tags) if request.tags else ""
        linked_ids = ",".join([entity.id for entity in request.linked_entities]) if request.linked_entities else ""
        
        metadata: Dict[str, Any] = {
            "memory_id": memory_id,
            "user_id": request.user_id,
            "workspace_id": request.workspace_id,
            "scope": request.scope.value,
            "type": request.type.value,
            "title": request.title,
            "tags": tags_str,
            "linked_ids": linked_ids,
            "status": request.status.value,
            "confidence": 1.0, # default confidence
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "usage_count": 0,
            "accepted_count": 0,
            "rejected_count": 0
        }
        
        # Build search-optimized document
        document = f"Title: {request.title}\n"
        document += f"Type: {request.type.value}\n"
        document += f"Summary: {request.summary}\n"
        document += f"Content: {request.content}\n"
        if tags_str:
            document += f"Tags: {tags_str}\n"
        if linked_ids:
            document += f"Linked Entities: {linked_ids}\n"

        self.store.upsert_memory(memory_id, document, metadata)
        
        return MemorySaveResponse(memory_id=memory_id, status="saved")

    def search_memory(self, request: MemorySearchRequest) -> MemorySearchResponse:
        where_conditions = [
            {"user_id": request.user_id},
            {"workspace_id": request.workspace_id}
        ]
        
        if request.filters:
            if request.filters.status:
                where_conditions.append({"status": request.filters.status})
            if request.filters.type:
                where_conditions.append({"type": request.filters.type})
        else:
            where_conditions.append({"status": "approved"})
            
        where = {"$and": where_conditions} if len(where_conditions) > 1 else where_conditions[0]
        
        results = self.store.query_memories(
            query_texts=[request.query],
            n_results=request.max_results,
            where=where
        )

        items = []
        if results and results.get('ids') and len(results['ids'][0]) > 0:
            ids = results['ids'][0]
            distances = results.get('distances', [[0.0] * len(ids)])[0]
            documents = results.get('documents', [[""] * len(ids)])[0]
            metadatas = results.get('metadatas', [[{}] * len(ids)])[0]
            
            for i in range(len(ids)):
                meta = metadatas[i]
                doc = documents[i]
                summary = ""
                title = meta.get("title", "")
                
                for line in doc.split("\n"):
                    if line.startswith("Summary: "):
                        summary = line.replace("Summary: ", "")
                        break
                        
                score = 1.0 / (1.0 + distances[i])
                
                item = SearchResultItem(
                    memory_id=ids[i],
                    title=title,
                    summary=summary,
                    score=score,
                    metadata=SearchResultMetadata(
                        type=meta.get("type", ""),
                        status=meta.get("status", ""),
                        linked_ids=meta.get("linked_ids")
                    )
                )
                items.append(item)
                
        return MemorySearchResponse(results=items)

    def suggest_related(self, request: MemorySuggestRequest) -> MemorySuggestResponse:
        where = {
            "$and": [
                {"user_id": request.user_id},
                {"workspace_id": request.workspace_id},
                {"status": {"$in": ["approved", "suggested", "draft"]}}
            ]
        }
        
        results = self.store.query_memories(
            query_texts=[request.current_query],
            n_results=20,
            where=where
        )

        suggestions = []
        if results and results.get('ids') and len(results['ids'][0]) > 0:
            ids = results['ids'][0]
            distances = results.get('distances', [[0.0] * len(ids)])[0]
            documents = results.get('documents', [[""] * len(ids)])[0]
            metadatas = results.get('metadatas', [[{}] * len(ids)])[0]
            
            for i in range(len(ids)):
                meta = metadatas[i]
                doc = documents[i]
                title = meta.get("title", "")
                
                if meta.get("status") in ["rejected", "archived"]:
                    continue
                
                score = calculate_score(distances[i], meta, request.linked_ids or [])
                
                if score >= 0.70:
                    reason = ""
                    if (request.linked_ids and meta.get("linked_ids") and 
                        any(r in meta.get("linked_ids", "") for r in request.linked_ids)):
                        reason = f"Matched linked ID and relevant task context."
                    else:
                        reason = f"Highly relevant to current query context."
                        
                    preview = ""
                    for line in doc.split("\n"):
                        if line.startswith("Content: "):
                            preview = line.replace("Content: ", "")[:100]
                            break
                            
                    suggestions.append({
                        "item": SuggestionItem(
                            memory_id=ids[i],
                            title=title,
                            reason=reason,
                            confidence=score,
                            preview=preview,
                            requires_approval=True
                        ),
                        "score": score
                    })
                    
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        final_items = [s["item"] for s in suggestions[:request.max_results]]
        
        if not final_items:
            return MemorySuggestResponse(suggestions=[], message="No strong related context found.")
            
        return MemorySuggestResponse(suggestions=final_items)

    def context_bundle(self, request: ContextBundleRequest) -> ContextBundleResponse:
        instructions = []
        source_ids = []
        
        for mem_id in request.memory_ids:
            mem = self.store.get_memory_by_id(mem_id)
            if not mem:
                continue
            
            meta = mem.get("metadata", {})
            if meta.get("user_id") != request.user_id or meta.get("workspace_id") != request.workspace_id:
                continue
                
            if meta.get("status") not in ["approved"]:
                continue
                
            doc = mem.get("document", "")
            content = ""
            for line in doc.split("\n"):
                if line.startswith("Content: "):
                    content = line.replace("Content: ", "")
                    break
                    
            if content:
                instructions.append(content)
                source_ids.append(mem_id)
                
        if not instructions:
            raise HTTPException(status_code=400, detail="No valid approved memories found for bundle.")
            
        return ContextBundleResponse(
            context_bundle=ContextBundle(
                bundle_id=f"bundle_{uuid.uuid4().hex}",
                instructions=instructions,
                source_memory_ids=source_ids
            )
        )
