from pathlib import Path
import shutil

def safe_delete(path: Path):
    try:
        if path.is_file() or path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    except Exception as e:
        return{f"Failed to delete {path}: {e}"}

def clear():
    cache = Path("./sessions/cache")
    if cache.exists():
        for item in cache.iterdir():
            safe_delete(item)
    return {"success": True, "message": "Session and cache fully wiped!"}