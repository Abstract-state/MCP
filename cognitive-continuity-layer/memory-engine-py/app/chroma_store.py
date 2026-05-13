import chromadb
import os
from typing import List, Dict, Any, Optional

DEFAULT_COLLECTION_NAME = "cognitive_memories"

class ChromaStore:
    def __init__(self, persist_directory: str = None):
        if not persist_directory:
            persist_directory = os.environ.get("CHROMA_PERSIST_DIRECTORY", "./chroma_data")
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.default_collection = self.client.get_or_create_collection(name=DEFAULT_COLLECTION_NAME)

    def get_collection(self, name: str):
        return self.client.get_or_create_collection(name=name)

    def upsert_memory(self, memory_id: str, document: str, metadata: Dict[str, Any], collection_name: str = DEFAULT_COLLECTION_NAME):
        collection = self.get_collection(collection_name) if collection_name != DEFAULT_COLLECTION_NAME else self.default_collection
        collection.upsert(
            ids=[memory_id],
            documents=[document],
            metadatas=[metadata]
        )

    def query_memories(self, query_texts: List[str], n_results: int = 5, where: Optional[Dict[str, Any]] = None, collection_name: str = DEFAULT_COLLECTION_NAME):
        collection = self.get_collection(collection_name) if collection_name != DEFAULT_COLLECTION_NAME else self.default_collection
        results = collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where
        )
        return results

    def get_memory_by_id(self, memory_id: str, collection_name: str = DEFAULT_COLLECTION_NAME):
        collection = self.get_collection(collection_name) if collection_name != DEFAULT_COLLECTION_NAME else self.default_collection
        result = collection.get(
            ids=[memory_id]
        )
        if not result or not result['ids']:
            return None
        return {
            'id': result['ids'][0],
            'document': result['documents'][0] if result['documents'] else None,
            'metadata': result['metadatas'][0] if result['metadatas'] else None
        }

