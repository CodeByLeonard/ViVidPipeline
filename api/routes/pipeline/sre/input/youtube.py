import re

from yt_dlp import YoutubeDL
from routes.pipeline.sre.session.session import Clip, current_session


def is_vaild_youtube_id(youtube_id: str) -> bool:
    return bool(re.compile(r"^[a-zA-Z0-9_-]{11}$").fullmatch(youtube_id))

def handle_download(youtube_id: str):
    if not (is_vaild_youtube_id(youtube_id)):
        return {"status": "failed", "message": "This is not a valid YouTube ID"}

    from main import cache
    result = None

    def progress_hook(data):
        nonlocal result
        if data["status"] == "finished":
            result = data
        return None

    params: dict = {
        "overwrites": True,
        "nopart": True,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": f"{cache}/clip_{youtube_id}.%(ext)s",
        "progress_hooks": [progress_hook],
    }

    with YoutubeDL(params=params) as yt:
        info = yt.extract_info(f"https://youtube.com/watch?v={youtube_id}", download=True)
        filename = yt.prepare_filename(info)

        if filename.endswith(".webm"):
            filename = filename[:-5] + ".mp4"

    if result is not None:
        info = result["info_dict"]
        clip = Clip(
            info["id"],
            filename,
            info["title"],
            info["description"],
            info["like_count"],
            info["view_count"],
        )
        current_session.clip = clip
        return clip
    else:
        return "Well, this shouldn't happen..."