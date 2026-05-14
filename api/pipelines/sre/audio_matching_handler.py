from fastapi import APIRouter, HTTPException

from proc.sre.audio_matching.modules.corrections import correct, CorrectionsRequest
from proc.sre.audio_matching.scope import ScopeRequest, define_scope
from proc.sre.session.initialize import get_session

router = APIRouter(prefix="/am")

@router.post("/scope")
async def scope_request(request: ScopeRequest):
    return await define_scope(request)

@router.get("/run")
async def matcher_run():
    if not get_session().status.stage == "matching":
        return "The session is not at the matching step. Perhaps a scope is needed first!"

    from proc.sre.audio_matching.main import main as matcher_main
    matcher_main()
    get_session().status.stage = "manual review"
    return "Finished."

@router.post("/correct")
async def matcher_correct(request: CorrectionsRequest):
    return await correct(request)