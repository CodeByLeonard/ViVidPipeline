from pathlib import Path

from fastapi import APIRouter, HTTPException

from proc.sre.audio_matching.modules.corrections import correct, CorrectionsRequest
from proc.sre.audio_matching.modules.matcher import load_matches
from proc.sre.audio_matching.scope import ScopeRequest, define_scope, load_scope
from proc.sre.session.initialize import get_session

router = APIRouter(prefix="/am")

@router.post("/scope")
async def scope_request(request: ScopeRequest):
    return await define_scope(request)

@router.get("/run")
async def matcher_run():
    if not get_session().status.stage == "matching":
        return "The session is not at the matching step."

    from proc.sre.audio_matching.main import main as matcher_main
    matcher_return = matcher_main()
    get_session().status.stage = "manual review"
    return matcher_return

@router.post("/correct")
async def matcher_correct(request: CorrectionsRequest):
    return await correct(request)

@router.get("/status")
async def status_request():
    if Path("./sessions/sre/segmentation/scope.json").exists():
        scope = load_scope()
    else: scope = ""

    if Path("./sessions/sre/segmentation/matches.json").exists():
        matches = load_matches()
    else: matches = ""

    return {"scope": scope, "matches": matches}