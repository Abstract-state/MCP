import pytest
from fastapi.testclient import TestClient

from app.main import app, get_memory_service
from app.memory_service import MemoryService
from app.chroma_store import ChromaStore

@pytest.fixture
def test_client(tmp_path):
    store = ChromaStore(persist_directory=str(tmp_path))
    service = MemoryService(store=store)
    
    app.dependency_overrides[get_memory_service] = lambda: service
    client = TestClient(app)
    
    # Pre-populate memories
    client.post("/memory/save", json={
        "user_id": "u_001", "workspace_id": "ws_1", "type": "task_context",
        "title": "Minimal DAX fix style", "summary": "DAX rules", "content": "Use DAX variables.",
        "tags": ["dax"], "linked_entities": [{"type": "jira", "id": "BI-482"}],
        "scope": "private", "status": "approved"
    })
    
    # A rejected memory to ensure it's filtered
    client.post("/memory/save", json={
        "user_id": "u_001", "workspace_id": "ws_1", "type": "task_context",
        "title": "Bad DAX style", "summary": "Bad DAX rules", "content": "Bad.",
        "tags": ["dax"], "linked_entities": [{"type": "jira", "id": "BI-482"}],
        "scope": "private", "status": "rejected"
    })
    
    # A memory for another user
    client.post("/memory/save", json={
        "user_id": "u_002", "workspace_id": "ws_1", "type": "task_context",
        "title": "Other DAX", "summary": "DAX rules", "content": "Other.",
        "tags": ["dax"], "linked_entities": [{"type": "jira", "id": "BI-482"}],
        "scope": "private", "status": "approved"
    })
    
    yield client, store
    app.dependency_overrides.clear()

def test_suggest_returns_dax_memory(test_client):
    client, store = test_client
    payload = {
        "user_id": "u_001",
        "workspace_id": "ws_1",
        "current_query": "Minimal DAX fix style DAX rules Use DAX variables.",
        "linked_ids": ["BI-482"],
        "max_results": 3
    }
    
    response = client.post("/memory/suggest", json=payload)
    assert response.status_code == 200
    suggestions = response.json()["suggestions"]
    assert len(suggestions) > 0
    assert suggestions[0]["title"] == "Minimal DAX fix style"
    assert "reason" in suggestions[0]
    assert suggestions[0]["confidence"] >= 0.70

def test_suggest_excludes_rejected(test_client):
    client, store = test_client
    payload = {
        "user_id": "u_001",
        "workspace_id": "ws_1",
        "current_query": "Bad DAX",
        "max_results": 3
    }
    
    response = client.post("/memory/suggest", json=payload)
    assert response.status_code == 200
    titles = [s["title"] for s in response.json()["suggestions"]]
    assert "Bad DAX style" not in titles
