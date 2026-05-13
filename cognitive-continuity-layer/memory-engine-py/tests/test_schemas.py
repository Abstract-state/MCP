import pytest
from pydantic import ValidationError
from app.schemas import (
    MemorySaveRequest,
    MemorySearchRequest,
    MemorySuggestRequest,
    ContextBundleRequest,
    MemoryType,
    MemoryStatus,
    MemoryScope
)

def test_memory_save_valid():
    req = MemorySaveRequest(
        user_id="u_001",
        workspace_id="ws_001",
        type=MemoryType.task_context,
        title="Valid title",
        summary="Valid summary",
        content="Valid content",
        scope=MemoryScope.private,
        status=MemoryStatus.approved
    )
    assert req.user_id == "u_001"

def test_memory_save_invalid_title():
    with pytest.raises(ValidationError):
        MemorySaveRequest(
            user_id="u_001",
            workspace_id="ws_001",
            type=MemoryType.task_context,
            title="A" * 121, # over 120
            summary="Valid summary",
            content="Valid content",
            scope=MemoryScope.private,
            status=MemoryStatus.approved
        )

def test_memory_save_invalid_enum():
    with pytest.raises(ValidationError):
        MemorySaveRequest(
            user_id="u_001",
            workspace_id="ws_001",
            type="invalid_type",
            title="Valid title",
            summary="Valid summary",
            content="Valid content",
            scope=MemoryScope.private,
            status=MemoryStatus.approved
        )

def test_memory_search_valid():
    req = MemorySearchRequest(
        user_id="u_001",
        workspace_id="ws_001",
        query="fix DAX",
        max_results=5
    )
    assert req.query == "fix DAX"

def test_memory_search_invalid_query():
    with pytest.raises(ValidationError):
        MemorySearchRequest(
            user_id="u_001",
            workspace_id="ws_001",
            query="fi", # less than 3
            max_results=5
        )

def test_memory_search_invalid_max_results():
    with pytest.raises(ValidationError):
        MemorySearchRequest(
            user_id="u_001",
            workspace_id="ws_001",
            query="fix DAX",
            max_results=25 # over 20
        )

def test_memory_suggest_valid():
    req = MemorySuggestRequest(
        user_id="u_001",
        workspace_id="ws_001",
        current_query="Can you fix this DAX?"
    )
    assert req.current_query == "Can you fix this DAX?"

def test_memory_suggest_invalid_query():
    with pytest.raises(ValidationError):
        MemorySuggestRequest(
            user_id="u_001",
            workspace_id="ws_001",
            current_query="Ca" # less than 3
        )

def test_context_bundle_valid():
    req = ContextBundleRequest(
        user_id="u_001",
        workspace_id="ws_001",
        memory_ids=["mem_1", "mem_2"]
    )
    assert len(req.memory_ids) == 2

def test_context_bundle_invalid_memory_ids_max():
    with pytest.raises(ValidationError):
        ContextBundleRequest(
            user_id="u_001",
            workspace_id="ws_001",
            memory_ids=["m1", "m2", "m3", "m4", "m5", "m6"] # over 5
        )

def test_context_bundle_invalid_memory_ids_min():
    with pytest.raises(ValidationError):
        ContextBundleRequest(
            user_id="u_001",
            workspace_id="ws_001",
            memory_ids=[] # less than 1
        )
