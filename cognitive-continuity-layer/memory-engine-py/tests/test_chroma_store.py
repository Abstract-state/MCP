import pytest
from app.chroma_store import ChromaStore

@pytest.fixture
def temp_chroma(tmp_path):
    store = ChromaStore(persist_directory=str(tmp_path))
    yield store

def test_upsert_and_get_memory(temp_chroma):
    mem_id = "mem_123"
    doc = "Title: Test Memory\nContent: This is a test."
    meta = {
        "user_id": "u_001",
        "workspace_id": "ws_001",
        "type": "task_context",
        "status": "approved"
    }
    
    temp_chroma.upsert_memory(mem_id, doc, meta)
    
    fetched = temp_chroma.get_memory_by_id(mem_id)
    assert fetched is not None
    assert fetched['id'] == mem_id
    assert fetched['document'] == doc
    assert fetched['metadata'] == meta

def test_query_memories(temp_chroma):
    temp_chroma.upsert_memory("mem_1", "apples are red", {"type": "fruit", "status": "approved"})
    temp_chroma.upsert_memory("mem_2", "bananas are yellow", {"type": "fruit", "status": "draft"})
    
    results = temp_chroma.query_memories(["red apple"], n_results=1)
    
    assert results is not None
    assert len(results['ids'][0]) > 0
    assert results['ids'][0][0] == "mem_1"

def test_query_with_where_filter(temp_chroma):
    temp_chroma.upsert_memory("mem_1", "apples are red", {"type": "fruit", "status": "approved"})
    temp_chroma.upsert_memory("mem_2", "bananas are yellow", {"type": "fruit", "status": "approved"})
    
    results = temp_chroma.query_memories(
        query_texts=["fruit"], 
        n_results=2, 
        where={"status": "draft"}
    )
    assert len(results['ids'][0]) == 0

def test_persistence(tmp_path):
    store1 = ChromaStore(persist_directory=str(tmp_path))
    store1.upsert_memory("persist_1", "persistence test", {"status": "approved"})
    
    store2 = ChromaStore(persist_directory=str(tmp_path))
    fetched = store2.get_memory_by_id("persist_1")
    
    assert fetched is not None
    assert fetched['id'] == "persist_1"
    assert fetched['document'] == "persistence test"
