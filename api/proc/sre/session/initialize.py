import json
import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Tuple

from yt_dlp.utils import DownloadError

from proc.preview.youtube import download_youtube
from proc.sre.session.ffprobe import get_video_metadata
from proc.sre.session.paths import initialize_workspace, reset_workspace

SESSION_FILEPATH = Path("./sessions/sre")

class Original(BaseModel):
    filepath: str
    fps: float
    resolution: Tuple[int, int]

class Clip(BaseModel):
    filepath: str
    youtube_id: str
    title: str = ""
    description: str = ""
    likes: int = 0
    views: int = 0

class SessionData(BaseModel):
    original: Original
    clip: Clip

class SessionStatus(BaseModel):
    stage: str
    state: str
    current_task: str

class Session(BaseModel):
    id: str
    title: str
    created_at: datetime

    session_data: SessionData
    status: SessionStatus
    version: int = 1

def create_session_json(
        title: str,
        original_filepath: str,
        fps: float,
        resolution: tuple[int, int],
        clip_filepath: str,
        youtube_id: str,
) -> Session:
    session = Session(
        id=str(uuid.uuid4()),
        title=title,
        created_at=datetime.now(),

        session_data=SessionData(
            original=Original(filepath=original_filepath, fps=fps, resolution=resolution),
            clip=Clip(filepath=clip_filepath, youtube_id=youtube_id),
        ),

        status=SessionStatus(
            stage="scope",
            state="",
            current_task="",
        ),
        version=1
    )

    with open(SESSION_FILEPATH / "session.json", "w") as f:
        json.dump(session.model_dump(mode="json"), f, indent=2)
    return session

async def initialize(
        title: str,
        youtube_id: str,
        original_file: UploadFile
):
    initialize_workspace()

    original_file_ext = Path(str(original_file.filename)).suffix
    original_filepath = SESSION_FILEPATH / f"input/original{original_file_ext}"
    with open(str(original_filepath), "wb") as f:
        f.write(await original_file.read())

    clip_filepath = SESSION_FILEPATH / "input/clip.mp4"
    try: download_youtube(youtube_id, str(clip_filepath))
    except DownloadError as e:
        reset_workspace()
        raise HTTPException(status_code=400, detail="YouTube download failed (Sign in to confirm you're not a bot).")

    fps, resolution = get_video_metadata(str(original_filepath))

    session = create_session_json(
        title=title,
        original_filepath=str(original_filepath),
        fps=fps,
        resolution=resolution,
        clip_filepath=str(clip_filepath),
        youtube_id=youtube_id,
    )
    return session

def get_session() -> Session:
    session_path = SESSION_FILEPATH / "session.json"

    if not session_path.exists():
        raise FileNotFoundError("Session does not exist")

    with open(session_path, "r") as f:
        data = json.load(f)

    return Session.model_validate(data)

def save_session(session: Session):
    session_path = SESSION_FILEPATH / "session.json"

    with open(session_path, "w") as f:
        json.dump(
            session.model_dump(mode="json"),
            f,
            indent=2
        )