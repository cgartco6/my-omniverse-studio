from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class StudioSessionMetadata(BaseModel):
    session_id: str = Field(..., description="Unique generated UUID identifier key for transaction audit tracking")
    text_prompt: str = Field(..., description="User textual layout description input describing music tone")
    genre_mix: str = Field(..., description="Target genre blend structure mapped manually to preference matrices")
    target_bpm: int = Field(120, ge=60, le=220, description="Clock frequency track pacing tempo reference metric")

class VectorQueryResponse(BaseModel):
    historical_profile: str
    meta: Dict[str, str]

class OrchestratorOutput(BaseModel):
    session_id: str
    status: str
    memory_context_applied: List[VectorQueryResponse]
    audio_route: str
    video_route: str
