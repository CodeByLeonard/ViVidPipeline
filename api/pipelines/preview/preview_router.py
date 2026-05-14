from fastapi import APIRouter

from pipelines.preview.clear_cache import clear
from pipelines.preview.youtube import handle_download

router = APIRouter(prefix="/preview")

@router.get("/")
def list_pipelines():
    return description

description = {
    "id": 0,
    "title": "Preview",
    "status": "PROTOTYPE" # later maybe ONLINE or OPERATIONAL
}

@router.get("/youtube/{youtube_id}")
def youtube(youtube_id: str):
    return handle_download(youtube_id)

@router.get("/clear")
def clear_cache():
    return clear()