import json
from pathlib import Path

from pydantic import BaseModel
from scenedetect import detect, AdaptiveDetector, split_video_ffmpeg
from proc.sre.session.initialize import get_session
from proc.sre.session.paths import CLIP_SEGMENTS

VIDEO_SEGMENTS_FILEPATH = Path("./sessions/sre/segmentation/video_segments.json")

class VideoSegment(BaseModel):
    index: int
    clip_start: float
    clip_end: float
    duration: float

class VideoSegmentFile(BaseModel):
    video_segments: list[VideoSegment]

def save_video_segments(file: VideoSegmentFile):
    VIDEO_SEGMENTS_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    with open(VIDEO_SEGMENTS_FILEPATH, "w") as f:
        json.dump(file.model_dump(mode="json"), f, indent=2)

def load_video_segments() -> VideoSegmentFile:
    with open(VIDEO_SEGMENTS_FILEPATH, "r") as f:
        data = json.load(f)
    return VideoSegmentFile.model_validate(data)


def get_segments(filepath):
    scene_list = detect(filepath, AdaptiveDetector())
    return scene_list

def clip_cut_detect():
    scene_list = get_segments(get_session().session_data.clip.filepath)
    split_video_ffmpeg(get_session().session_data.clip.filepath, scene_list, str(CLIP_SEGMENTS))

    segments: list[VideoSegment] = []
    for index, (scene_start, scene_end) in enumerate(scene_list):
        segments.append(
            VideoSegment(
                index=index,
                clip_start=scene_start.seconds,
                clip_end=scene_end.seconds,
                duration=(scene_end.seconds - scene_start.seconds)
            )
        )
    save_video_segments(VideoSegmentFile(video_segments=segments))