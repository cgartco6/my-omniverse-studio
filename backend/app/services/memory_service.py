import numpy as np
from chromadb import Client, Settings

class LongTermMemoryManager:
    """
    Maintains user's musical preferences, historical prompt weights, 
    and acoustic fingerprints of uploaded voice samples over time.
    """
    def __init__(self):
        # Initializing local vector database for persistent context caching
        self.chroma_client = Client(Settings(persist_directory="./.memory_vault"))
        self.collection = self.chroma_client.get_or_create_collection(name="studio_memory")

    def remember_session(self, user_id: str, prompt_meta: dict, embedding: list[float]):
        """Saves current musical weights, genres, and context fingerprints."""
        self.collection.add(
            embeddings=[embedding],
            metadatas=[prompt_meta],
            ids=[f"session_{user_id}_{prompt_meta['timestamp']}"]
        )

    def recall_context(self, current_prompt_embedding: list[float], limit: int = 3):
        """Retrieves past sessions that match the target musical style or asset footprint."""
        results = self.collection.query(
            query_embeddings=[current_prompt_embedding],
            n_results=limit
        )
        return results['metadatas']
