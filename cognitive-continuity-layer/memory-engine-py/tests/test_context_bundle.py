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
    yield client, store
    app.dependency_overrides.clear()

def test_context_bundle_valid(test_client):
    client, store = test_client
    # Save memory
    res = client.post("/memory/save", json={
        "user_id": "u_001", "workspace_id": "ws_1", "type": "task_context",
        "title": "Test Instruction", "summary": "test", "content": "Do this always.",
        "scope": "private", "status": "approved"
    })
    mem_id = res.json()["memory_id"]
    
    # Request bundle
    bundle_res = client.post("/context/bundle", json={
        "user_id": "u_001",
        "workspace_id": "ws_1",
        "memory_ids": [mem_id]
    })
    assert bundle_res.status_code == 200
    bundle = bundle_res.json()["context_bundle"]
    assert mem_id in bundle["source_memory_ids"]
    assert "Do this always." in bundle["instructions"]

def test_context_bundle_rejects_rejected(test_client):
    client, store = test_client
    res = client.post("/memory/save", json={
        "user_id": "u_001", "workspace_id": "ws_1", "type": "task_context",
        "title": "Bad Instruction", "summary": "test", "content": "Do not do this.",
        "scope": "private", "status": "rejected"
    })
    mem_id = res.json()["memory_id"]
    
    bundle_res = client.post("/context/bundle", json={
        "user_id": "u_001",
        "workspace_id": "ws_1",
        "memory_ids": [mem_id]
    })
    assert bundle_res.status_code == 400
