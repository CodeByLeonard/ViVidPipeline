from proc.sre.stages.session import get_session, save_session
from proc.sre.paths import SessionSRE
from fastapi import HTTPException
from pydantic import BaseModel
import json

class ScopeEntry(BaseModel):
    segment_id: int
    start: float
    end: float

class PresetEntry(BaseModel):
    speed: float
    language: str
    channel: str

class ParametersFile(BaseModel):
    preset: PresetEntry
    scopes: list[ScopeEntry]

class ParametersRequest(BaseModel):
    preset: PresetEntry
    scopes: list[ScopeEntry]

PARAMETERS_FILEPATH = SessionSRE.EXTRACTION.PARAMETERS_JSON

def save_params(params_file: ParametersFile):
    PARAMETERS_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PARAMETERS_FILEPATH, "w") as f:
        json.dump(params_file.model_dump(mode="json"), f, indent=2)

def load_params() -> ParametersFile:
    if not PARAMETERS_FILEPATH.exists():
        raise FileNotFoundError("Parameters JSON does not exist")
    with open(PARAMETERS_FILEPATH, "r") as f:
        data = json.load(f)
    return ParametersFile.model_validate(data)

async def init_params(request: ParametersRequest):
    session = get_session()

    if session.status.stage != "parameters":
        raise HTTPException(status_code=400, detail="Session is not in load process stage")

    params_file = ParametersFile(preset=request.preset, scopes=request.scopes)
    save_params(params_file)

    session.status.stage = "extraction"
    save_session(session)