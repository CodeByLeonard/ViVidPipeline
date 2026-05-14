from fastapi import APIRouter, Form, UploadFile, File

from pipelines.sre.segmentation.handler import status
from pipelines.sre.session.initialize import initialize
from pipelines.sre.session.reset import reset

router = APIRouter(prefix="/session")

@router.post("/init")
async def init_request(
        pipeline_type: str = Form(...),
        title: str = Form(...),
        youtube_id: str = Form(...),
        original_file: UploadFile = File(...)
): return await initialize(pipeline_type, title, youtube_id, original_file)

@router.get("/reset")
def reset_request():
    return reset()

@router.get("/status")
def status_request():
    return status()

