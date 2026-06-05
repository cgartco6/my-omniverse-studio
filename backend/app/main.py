import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.services.memory_service import AudioMemoryVault
from app.services.audio_processor import LocalAudioEngine
from app.services.ai_orchestrator import MultiModalStudioOrchestrator

app = FastAPI(title="Omniverse Multi-Modal Studio Generation Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_ROOT_DIRECTORY = os.path.abspath("./studio_storage")
os.makedirs(STORAGE_ROOT_DIRECTORY, exist_ok=True)

# Mount the media assets directory directly onto a static routing layer
app.mount("/static", StaticFiles(directory=STORAGE_ROOT_DIRECTORY), name="static")

vault_storage_path = os.path.join(STORAGE_ROOT_DIRECTORY, "vector_db")
memory_vault = AudioMemoryVault(persist_path=vault_storage_path)
audio_engine = LocalAudioEngine()
video_orchestrator = MultiModalStudioOrchestrator()

@app.post("/api/v1/ingest-workspace", status_code=status.HTTP_201_CREATED)
async def process_studio_pipeline(
    text_prompt: str = Form(...),
    genre_mix: str = Form(...),
    target_bpm: int = Form(120),
    vocal_file: UploadFile = File(None),
    image_file: UploadFile = File(None)
):
    session_id = str(uuid.uuid4())
    session_working_space = os.path.join(STORAGE_ROOT_DIRECTORY, session_id)
    os.makedirs(session_working_space, exist_ok=True)
    
    saved_vocal_path = None
    saved_image_path = None

    if vocal_file:
        saved_vocal_path = os.path.join(session_working_space, f"input_vocal_{uuid.uuid4().hex[:6]}.wav")
        with open(saved_vocal_path, "wb") as buffer:
            shutil.copyfileobj(vocal_file.file, buffer)
            
    if image_file:
        saved_image_path = os.path.join(session_working_space, f"reference_frame_{uuid.uuid4().hex[:6]}.jpg")
        with open(saved_image_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)

    # Long Term Context Processing
    style_query_string = f"{text_prompt} {genre_mix}"
    historical_context_data = memory_vault.recall_sonic_history(query_text=style_query_string, limit=3)
    
    # Engine Computation Layer Execution loops
    master_audio_filename = "output_master_mix.wav"
    master_video_filename = "output_video_canvas.mp4"
    
    full_audio_output_path = os.path.join(session_working_space, master_audio_filename)
    full_video_output_path = os.path.join(session_working_space, master_video_filename)

    audio_engine.mix_and_render_track(
        text_prompt=text_prompt,
        target_bpm=target_bpm,
        output_path=full_audio_output_path,
        user_voice_path=saved_vocal_path
    )
    
    video_orchestrator.synthesize_visual_accompaniment(
        prompt=genre_mix,
        input_image_path=saved_image_path,
        target_output_video_path=full_video_output_path
    )

    memory_vault.commit_session_to_memory(
        session_id=session_id,
        text_prompt=text_prompt,
        genre_mix=genre_mix,
        bpm=target_bpm
    )
    
    return {
        "session_id": session_id,
        "status": "COMPILATION COMPLETE",
        "memory_context_applied": historical_context_data,
        "assets": {
            "master_audio_route": f"http://localhost:8000/static/{session_id}/{master_audio_filename}",
            "master_video_route": f"http://localhost:8000/static/{session_id}/{master_video_filename}"
        }
    }
