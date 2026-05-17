from proc.sre.paths import SessionSRE, reset_workspace, initialize_workspace
from proc.preview.youtube import download_youtube
from fastapi import UploadFile, HTTPException
from yt_dlp.utils import DownloadError
from pydantic import BaseModel
from datetime import datetime
from typing import Tuple
from pathlib import Path
import subprocess
import json
import uuid

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

        status=SessionStatus(stage="parameters", state="", current_task=""),
        version=1
    )


    with open(SessionSRE.SESSION_JSON, "w") as f:
        json.dump(session.model_dump(mode="json"), f, indent=2)
    return session

async def save_original(original_file: UploadFile):
    original_file_ext = Path(str(original_file.filename)).suffix
    original_filepath = SessionSRE.ROOT / f"input/original{original_file_ext}"
    with open(str(original_filepath), "wb") as f:
        f.write(await original_file.read())
    return original_filepath

def save_clip(youtube_id: str):
    try:
        download_youtube(youtube_id, str(SessionSRE.INPUT.CLIP))
    except DownloadError as e:
        reset_workspace()
        raise HTTPException(status_code=400, detail="YouTube download failed (Sign in to confirm you're not a bot).")

async def init_session(
        title: str,
        youtube_id: str,
        original_file: UploadFile,
):
    initialize_workspace()

    original_filepath = await save_original(original_file)
    save_clip(youtube_id)

    fps, resolution = get_video_metadata(str(original_filepath))
    session = create_session_json(
        title=title,
        original_filepath=str(original_filepath),
        fps=fps,
        resolution=resolution,
        clip_filepath=str(SessionSRE.INPUT.CLIP),
        youtube_id=youtube_id,
    )

    return session

def get_session() -> Session:
    if not SessionSRE.SESSION_JSON.exists():
        raise FileNotFoundError("Session does not exist")

    with open(SessionSRE.SESSION_JSON, "r") as f:
        data = json.load(f)

    return Session.model_validate(data)

def save_session(session: Session):
    with open(SessionSRE.SESSION_JSON, "w") as f:
        json.dump(session.model_dump(mode="json"), f, indent=2)

def get_video_metadata(filepath: str) -> tuple[float, tuple[int, int]]:
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries",
        "stream=r_frame_rate,width,height",
        "-of", "json",
        filepath
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)

    stream = data["streams"][0]

    width = stream["width"]
    height = stream["height"]

    fps_raw = stream["r_frame_rate"]

    numerator, denominator = map(int, fps_raw.split("/"))
    fps = numerator / denominator

    return fps, (width, height)