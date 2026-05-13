import pytest
from fastapi.testclient import TestClient

from app.main import app, get_memory_service
from app.memory_service import MemoryService
from app.chroma_store import ChromaStore

@pytest.fixture
def test_client(tmp_path):
    store = ChromaStore(persist_directory=str(tmp_path))
    service = MemoryService(store=store)
    
    # Override dependency
    app.dependency_overrides[get_memory_service] = lambda: service
    client = TestClient(app)
    
    yield client, store
    
    # Clear overrides
    app.dependency_overrides.clear()

def test_save_memory_valid(test_client):
    client, store = test_client
    payload = {
        "user_id": "u_001",
        "workspace_id": "corp_ws",
        "type": "task_context",
        "title": "Minimal DAX fix style",
        "summary": "User prefers minimal logic changes for DAX fixes.",
        "content": "Preserve measure names, avoid refactoring, return corrected DAX first.",
        "tags": ["dax", "minimal-change", "formatting"],
        "linked_entities": [
            { "type": "jira", "id": "BI-482" },
            { "type": "project", "id": "analytics-reporting" }
        ],
        "scope": "private",
        "status": "approved"
    }
    
    response = client.post("/memory/save", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "saved"
    memory_id = data["memory_id"]
    assert memory_id.startswith("mem_")
    
    # Check if metadata stored correctly
    saved_memory = store.get_memory_by_id(memory_id)
    assert saved_memory is not None
    metadata = saved_memory["metadata"]
    assert metadata["user_id"] == "u_001"
    assert metadata["tags"] == "dax,minimal-change,formatting"
    assert metadata["linked_ids"] == "BI-482,analytics-reporting"
    assert "Minimal DAX fix style" in saved_memory["document"]

def test_save_memory_invalid(test_client):
    client, store = test_client
    payload = {
        "user_id": "u_001"
        # missing workspace_id and others
    }
    response = client.post("/memory/save", json=payload)
    assert response.status_code == 422 # Pydantic Validation error
