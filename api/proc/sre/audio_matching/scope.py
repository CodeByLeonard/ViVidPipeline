from proc.sre.session.initialize import get_session, save_session
from fastapi import HTTPException

from pydantic import BaseModel
from pathlib import Path
import json

SCOPE_FILEPATH = Path("./sessions/sre/segmentation/scope.json")

class ScopeEntry(BaseModel):
    segment_id: int
    start: float
    end: float

class ScopeFile(BaseModel):
    scopes: list[ScopeEntry]

def save_scope(scope: ScopeFile):
    SCOPE_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SCOPE_FILEPATH, "w") as f:
        json.dump(scope.model_dump(mode="json"), f, indent=2)

def load_scope() -> ScopeFile:
    if not SCOPE_FILEPATH.exists():
        raise FileNotFoundError("Scope does not exist")
    with open(SCOPE_FILEPATH, "r") as f:
        data = json.load(f)
    return ScopeFile.model_validate(data)

class ScopeRequest(BaseModel):
    scopes: list[ScopeEntry]

async def define_scope(request: ScopeRequest):
    session = get_session()
    if session.status.stage != "scope":
        raise HTTPException(status_code=400, detail="Session is not in scope stage")

    scope = ScopeFile(scopes=request.scopes)
    save_scope(scope)

    session.status.stage = "matching"
    save_session(session)
    return "Saved the scope, now ready for matching!"

def get_scope_elements():
    from proc.sre.audio_matching.modules.source import AudioSource, Scope
    from proc.sre.session.paths import SessionSRE

    original_source = AudioSource(path=str(SessionSRE.EXTRACTION.ORIGINAL_MP3))
    clip_source = AudioSource(path=str(SessionSRE.EXTRACTION.CLIP_MP3))

    from proc.sre.audio_matching.scope import load_scope
    scope_file = load_scope()

    scope_segments = [ {"start": scope.start, "end": scope.end} for scope in scope_file.scopes ]
    scope = Scope(original_source, scope_segments)
    return original_source, clip_source, scope