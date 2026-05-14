import re
import starlette.status
from pathlib import Path
from yt_dlp import YoutubeDL

def is_valid_youtube_id(youtube_id: str) -> bool:
    return bool(re.compile(r"^[a-zA-Z0-9_-]{11}$").fullmatch(youtube_id))

def download_youtube(youtube_id: str, path: str):
    if not (is_valid_youtube_id(youtube_id)):
        return {starlette.status.HTTP_400_BAD_REQUEST}

    result = None
    def progress_hook(data):
        nonlocal result
        if data["status"] == "finished":
            result = data
        return None

    params: dict = {
        "overwrites": True,
        "nopart": True,
        "format": "bestvideo[vcodec^=avc1]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": f"{path}",
        "progress_hooks": [progress_hook],
    }

    with YoutubeDL(params=params) as yt:
        info = yt.extract_info(f"https://youtube.com/watch?v={youtube_id}", download=True)
        filename = yt.prepare_filename(info)

    if result is not None:
        return {"success": True, "filepath": f"{filename}"}
    else:
        return {"success": False, "error": "Well, this shouldn't happen..."}