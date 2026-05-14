from fastapi import APIRouter, UploadFile, File
from pipelines.sre.input.original import handle_original

router = APIRouter(prefix="/input")

@router.post("/original")
async def original(file: UploadFile = File(...)):
    return await handle_original(file)