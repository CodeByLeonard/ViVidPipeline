from fastapi import APIRouter, UploadFile, File
from routes.pipeline.sre.input.youtube import handle_download
from routes.pipeline.sre.input.original import handle_original

router = APIRouter(prefix="/input")

@router.get("/youtube/{youtube_id}")
def youtube(youtube_id: str):
    return handle_download(youtube_id)

@router.post("/original")
async def original(file: UploadFile = File(...)):
    return await handle_original(file)