from fastapi import APIRouter

from proc.preview.clear_cache import clear
from proc.preview.youtube import download_youtube

router = APIRouter(prefix="/preview")

@router.get("/")
def list_pipelines():
    return description

description = {
    "id": 0,
    "title": "Preview",
    "status": "PROTOTYPE" # later maybe ONLINE or OPERATIONAL
}

CACHE_PATH = "./sessions/cache"

@router.get("/youtube/{youtube_id}")
def youtube(youtube_id: str):
    return download_youtube(youtube_id, f"{CACHE_PATH}/{youtube_id}.mp4")

@router.get("/clear")
def clear_cache():
    return clear()