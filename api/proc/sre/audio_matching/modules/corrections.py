from proc.sre.session.initialize import get_session, save_session
from fastapi import HTTPException

from pydantic import BaseModel
from pathlib import Path
import json

CORRECTIONS_FILEPATH = Path("./sessions/sre/segmentation/corrections.json")

class MatchCorrectionEntry(BaseModel):
    match: int
    start_match: float
    end_match: float

class CorrectionsFile(BaseModel):
    match_corrections: list[MatchCorrectionEntry]

def save_corrections(scope: CorrectionsFile):
    CORRECTIONS_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CORRECTIONS_FILEPATH, "w") as f:
        json.dump(scope.model_dump(mode="json"), f, indent=2)

def load_corrections() -> CorrectionsFile:
    with open(CORRECTIONS_FILEPATH, "r") as f:
        data = json.load(f)
    return CorrectionsFile.model_validate(data)

class CorrectionsRequest(BaseModel):
    match_corrections: list[MatchCorrectionEntry]

async def correct(request: CorrectionsRequest):
    session = get_session()
    # if not session.status.stage == "manual review":
    #     return "The session is not at the manual review step."

    match_corrections = CorrectionsFile(match_corrections=request.match_corrections)
    save_corrections(match_corrections)

    session.status.stage = "matching"
    save_session(session)
    from proc.sre.audio_matching.main import rematch
    rematch()
    return "Saved the corrections and rematched!"