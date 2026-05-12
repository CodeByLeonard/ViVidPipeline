import shutil

from fastapi import APIRouter
from pathlib import Path
import shutil

from routes.pipeline.sre.session.session import current_session

router = APIRouter(prefix="/session")

@router.get("/initialize")
async def initialize():
    if (current_session.clip == None or current_session.original == None):
        return {"success": False, "message": "Clip or Original have not been set yet!"}

    current_session.active = True
    current_session.stage = 1
    return {"success": True, "current_session": current_session}

def safe_delete(path: Path):
    try:
        if path.is_file() or path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    except Exception as e:
        print(f"Failed to delete {path}: {e}")

@router.get("/reset")
def reset():
    cache = Path("./cache")
    if cache.exists():
        for item in cache.iterdir():
            safe_delete(item)

    current_session.active = False
    current_session.clip = None
    current_session.original = None
    return {"success": True, "message": "Session and cache fully wiped!"}

@router.get("/status")
def status():
    return {"current_session": current_session}
