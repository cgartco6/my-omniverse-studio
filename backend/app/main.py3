import os
import uuid
import json
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Local module relative imports
from app.services.memory_service import AudioMemoryVault
from app.services.audio_processor import LocalAudioEngine

app = FastAPI(title="Omniverse Studio Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Workspace directories for scratch disk writes
STORAGE_DIR = os.path.abspath("./studio_storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

# Initialize production services
vault = AudioMemoryVault(persist_path=os.path.join(STORAGE_DIR, "vector_db"))
audio_engine = LocalAudioEngine()

class SynthesisRequest(BaseModel):
    text_prompt: str
    genre_mix: str
    target_bpm: int

@app.post("/api/v1/ingest-workspace", status_code=status.HTTP_201_CREATED)
async def process_studio_pipeline(
    text_prompt: str = Form(...),
    genre_mix: str = Form(...),
    target_bpm: int = Form(120),
    vocal_file: Optional[UploadFile] = File(None),
    image_file: Optional[UploadFile] = File(None)
):
    """
    Direct multi-modal execution node. Processes uploads, updates long term state,
    and returns production asset references.
    """
    session_id = str(uuid.uuid4())
    session_path = os.path.join(STORAGE_DIR, session_id)
    os.makedirs(session_path, exist_ok=True)
    
    saved_vocal = None
    saved_image = None
    
    # 1. Physical file write layer
    if vocal_file:
        saved_vocal = os.path.join(session_path, f"raw_input_{vocal_file.filename}")
        with open(saved_vocal, "wb") as buffer:
            shutil.copyfileobj(vocal_file.file, buffer)
            
    if image_file:
        saved_image = os.path.join(session_path, f"visual_anchor_{image_file.filename}")
        with open(saved_image, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)

    # 2. Long Term Memory Context recall
    style_query = f"{text_prompt} {genre_mix}"
    historical_context = vault.recall_sonic_history(query_text=style_query, limit=2)
    
    # 3. Execution of the local generation stack
    output_audio_path = os.path.join(session_path, "output_master.wav")
    
    # Run the genuine processing engine modules
    audio_engine.generate_synthetic_stems(
        prompt=text_prompt,
        bpm=target_bpm,
        output_path=output_audio_path,
        vocal_reference_path=saved_vocal
    )
    
    # 4. Save metadata back to vector memory to continuously train the model's taste profile
    vault.commit_session_to_memory(
        session_id=session_id,
        text_prompt=text_prompt,
        genre_mix=genre_mix,
        bpm=target_bpm
    )
    
    return {
        "session_id": session_id,
        "status": "Render Complete",
        "memory_context_applied": historical_context,
        "assets": {
            "master_audio_route": f"/static/{session_id}/output_master.wav",
            "vocal_source_route": f"/static/{session_id}/raw_input_{vocal_file.filename}" if vocal_file else None
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
