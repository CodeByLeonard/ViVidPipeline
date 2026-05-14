import json
import uuid

from fastapi import UploadFile, HTTPException, Form
from pydantic import BaseModel
from datetime import datetime
from typing import Tuple

from pipelines.sre.session.paths import initialize_workspace


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
    type: str
    id: str
    title: str
    created_at: datetime

    session_data: SessionData
    status: SessionStatus
    version: int = 1

def create_session_json(
        session_type: str,
        title: str,
        original_filepath: str,
        fps: float,
        resolution: tuple[int, int],
        clip_filepath: str,
        youtube_id: str,
) -> Session:
    session = Session(
        type=session_type,
        id=str(uuid.uuid4()),
        title=title,
        created_at=datetime.now(),

        session_data=SessionData(
            original=Original(filepath=original_filepath, fps=fps, resolution=resolution),
            clip=Clip(filepath=clip_filepath, youtube_id=youtube_id),
        ),

        status=SessionStatus(
            stage="scope",
            state="processing",
            current_task="",
        ),
        version=1
    )

    with open("./session/session.json", "w") as f:
        json.dump(session.model_dump(mode="json"), f, indent=2)
    return session

async def initialize(
        session_type: str="sre",
        title: str="The Rookie Dim and Juicy",
        youtube_id: str="Eon2EqOfGbs",
        original_file: UploadFile = Form(...)
):
    initialize_workspace()

    with open("./session/input/original.mkv", "wb") as f:
        f.write(await original_file.read())

    # TODO: ADD YOUTUBE DOWNLOAD HERE

    original_filepath = "./session/input/original.mkv"
    fps=23.976
    resolution: tuple[int, int] = (1920, 1080)
    clip_filepath = "./session/input/clip.mp4"

    session = create_session_json(
        session_type=session_type,
        title=title,
        original_filepath=original_filepath,
        fps=fps,
        resolution=resolution,
        clip_filepath=clip_filepath,
        youtube_id=youtube_id,
    )
    return session