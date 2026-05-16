from pathlib import Path

from fastapi import APIRouter, Form, UploadFile, File
from starlette.status import HTTP_200_OK

from proc.sre.stages.session import init_session, get_session
from proc.sre.paths import reset_workspace

router = APIRouter(prefix="/session")

@router.post("/init")
async def init_request(
        title: str = Form(...), youtube_id: str = Form(...), original_file: UploadFile = File(...),
):
    if Path("./sessions/sre").exists(): return {"A session has already been initialized, it was not overwritten!"}
    return await init_session(title, youtube_id, original_file)

@router.get("/reset")
def reset_request():
    reset_workspace()
    return HTTP_200_OK

@router.get("/status")
def status_request():
    return get_session()
