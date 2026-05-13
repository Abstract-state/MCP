import pytest
from fastapi.testclient import TestClient

from app.main import app, get_memory_service
from app.memory_service import MemoryService
from app.chroma_store import ChromaStore

@pytest.fixture
def integration_client(tmp_path):
    store = ChromaStore(persist_directory=str(tmp_path))
    service = MemoryService(store=store)
    
    app.dependency_overrides[get_memory_service] = lambda: service
    client = TestClient(app)
    
    yield client
    app.dependency_overrides.clear()

def test_full_save_search_suggest_bundle_flow(integration_client):
    client = integration_client
    
    # 1. SAVE Flow
    save_payload = {
        "user_id": "test_user",
        "workspace_id": "test_ws",
        "type": "task_context",
        "title": "Integration Test Pattern",
        "summary": "Rules for integration testing",
        "content": "Always validate the complete flow end-to-end.",
        "tags": ["testing", "integration"],
        "linked_entities": [{"type": "jira", "id": "TEST-123"}],
        "scope": "private",
        "status": "approved"
    }
    save_res = client.post("/memory/save", json=save_payload)
    assert save_res.status_code == 200, save_res.text
    mem_id = save_res.json()["memory_id"]
    
    # 2. SEARCH Flow
    search_payload = {
        "user_id": "test_user",
        "workspace_id": "test_ws",
        "query": "integration testing flow",
        "max_results": 5
    }
    search_res = client.post("/memory/search", json=search_payload)
    assert search_res.status_code == 200
    search_data = search_res.json()["results"]
    assert any(r["memory_id"] == mem_id for r in search_data)
    
    # 3. SUGGEST Flow
    suggest_payload = {
        "user_id": "test_user",
        "workspace_id": "test_ws",
        "current_query": "Integration Test Pattern Rules for integration testing",
        "linked_ids": ["TEST-123"],
        "max_results": 3
    }
    suggest_res = client.post("/memory/suggest", json=suggest_payload)
    assert suggest_res.status_code == 200
    suggest_data = suggest_res.json()["suggestions"]
    assert any(s["memory_id"] == mem_id for s in suggest_data)
    
    # 4. CONTEXT BUNDLE Flow
    bundle_payload = {
        "user_id": "test_user",
        "workspace_id": "test_ws",
        "memory_ids": [mem_id]
    }
    bundle_res = client.post("/context/bundle", json=bundle_payload)
    assert bundle_res.status_code == 200
    bundle_data = bundle_res.json()["context_bundle"]
    assert mem_id in bundle_data["source_memory_ids"]
    assert "Always validate the complete flow end-to-end." in bundle_data["instructions"]
