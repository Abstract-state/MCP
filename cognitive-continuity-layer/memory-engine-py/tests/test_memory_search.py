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
    
    # Pre-populate some memories
    client.post("/memory/save", json={
        "user_id": "u_001", "workspace_id": "ws_1", "type": "task_context",
        "title": "React context", "summary": "React rules", "content": "Use functional components.",
        "scope": "private", "status": "approved"
    })
    client.post("/memory/save", json={
        "user_id": "u_001", "workspace_id": "ws_1", "type": "task_context",
        "title": "Angular context", "summary": "Angular rules", "content": "Use classes.",
        "scope": "private", "status": "rejected"
    })
    client.post("/memory/save", json={
        "user_id": "u_002", "workspace_id": "ws_1", "type": "task_context",
        "title": "Vue context", "summary": "Vue rules", "content": "Use composition API.",
        "scope": "private", "status": "approved"
    })
    
    yield client, store
    app.dependency_overrides.clear()

def test_search_memory_returns_relevant_and_approved(test_client):
    client, store = test_client
    
    payload = {
        "user_id": "u_001",
        "workspace_id": "ws_1",
        "query": "React components",
        "max_results": 5
    }
    
    response = client.post("/memory/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    results = data["results"]
    assert len(results) == 1
    assert results[0]["title"] == "React context"
    assert results[0]["metadata"]["status"] == "approved"

def test_search_memory_excludes_rejected_by_default(test_client):
    client, store = test_client
    
    payload = {
        "user_id": "u_001",
        "workspace_id": "ws_1",
        "query": "Angular classes",
        "max_results": 5
    }
    
    response = client.post("/memory/search", json=payload)
    assert response.status_code == 200
    results = response.json()["results"]
    # Should not return Angular because it's rejected
    titles = [r["title"] for r in results]
    assert "Angular context" not in titles

def test_search_memory_respects_user_isolation(test_client):
    client, store = test_client
    
    payload = {
        "user_id": "u_001",
        "workspace_id": "ws_1",
        "query": "Vue rules",
        "max_results": 5
    }
    
    response = client.post("/memory/search", json=payload)
    assert response.status_code == 200
    results = response.json()["results"]
    # Should not return Vue because it belongs to u_002
    titles = [r["title"] for r in results]
    assert "Vue context" not in titles

def test_search_memory_max_results(test_client):
    client, store = test_client
    
    # Add more memories
    for i in range(5):
        client.post("/memory/save", json={
            "user_id": "u_001", "workspace_id": "ws_1", "type": "task_context",
            "title": f"Test {i}", "summary": "test", "content": "test",
            "scope": "private", "status": "approved"
        })
        
    payload = {
        "user_id": "u_001",
        "workspace_id": "ws_1",
        "query": "Test",
        "max_results": 2
    }
    
    response = client.post("/memory/search", json=payload)
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 2
