from fastapi import APIRouter
from yt_dlp import YoutubeDL

router = APIRouter(prefix="/reconstruct")


class Clip:
    def __init__(self, id, filename, title, desc, likes, views):
        self.id = id
        self.filename = filename
        self.title = title
        self.desc = desc
        self.likes = likes
        self.views = views


@router.get("/{youtube_id}")
def read_item(youtube_id: str):
    from main import cache

    result = None

    def progress_hook(data):
        nonlocal result
        if data["status"] == "finished":
            result = data
        return None

    with YoutubeDL(
        params={
            "format": "mp4/bestaudio/best",
            "outtmpl": f"{cache}/clip_{youtube_id}.%(ext)s",
            "progress_hooks": [progress_hook],
        }
    ) as yt:
        # WARN: DANGEROUS
        yt.download(f"https://youtube.com/watch?v={youtube_id}")

    if result is not None:
        info = result["info_dict"]
        clip = Clip(
            info["id"],
            result["filename"],
            info["title"],
            info["description"],
            info["like_count"],
            info["view_count"],
        )
        return clip
    else:
        return "Well, this shouldn't happen..."
