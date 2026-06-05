import os
import json
import chromadb
from chromadb.config import Settings

class AudioMemoryVault:
    """
    Manages vector representations of musical settings, prompt metadata, 
    and genre blends directly on your storage disk.
    """
    def __init__(self, persist_path: str):
        self.persist_path = os.path.abspath(persist_path)
        os.makedirs(self.persist_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_path)
        self.collection = self.client.get_or_create_collection(
            name="owner_stylistic_footprints"
        )

    def commit_session_to_memory(self, session_id: str, text_prompt: str, genre_mix: str, bpm: int):
        """Stores the structural parameters of your musical output into vector memory."""
        combined_document = f"Prompt Matrix Context: {text_prompt} | Blended Sub-Genres: {genre_mix} | Master Clock Sync Pace: {bpm}BPM"
        
        self.collection.add(
            documents=[combined_document],
            metadatas=[{
                "session_id": str(session_id),
                "genre_mix": str(genre_mix),
                "bpm": str(bpm)
            }],
            ids=[f"id_{session_id}"]
        )

    def recall_sonic_history(self, query_text: str, limit: int = 2) -> list:
        """Retrieves past sessions that match your stylistic goals."""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=limit
            )
            compiled_history = []
            if results and 'documents' in results and results['documents'] and len(results['documents']) > 0:
                for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                    compiled_history.append({
                        "historical_profile": str(doc),
                        "meta": {k: str(v) for k, v in meta.items()}
                    })
            return compiled_history
        except Exception:
            return []
