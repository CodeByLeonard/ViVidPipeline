from fastapi import APIRouter

from proc.segmentatioon.PySceneDetect import get_segments
from routes.pipeline.sre.segmentation.segment import Segment
from routes.pipeline.sre.session.session import current_session

router = APIRouter(prefix="/segmentation")

@router.get("/status")
def status():
    if len(current_session.clip_segments) == 0:
        return {"status": None}
    return {"status": "OK", "segments": current_session.clip_segments}

@router.get("/run")
def run():
    if (current_session.active is False): return {"success": False, "message": "The Session is not active"}
    if (current_session.clip is None): return {"success": False, "message": "No clip found in session"}
    divide_clip()

    from proc.audio_engineering.match_segment_original import match_segment_original
    match_segment_original()

    return {"segments": current_session.clip_segments}

def divide_clip():
    scene_list = get_segments()
    for index, (scene_start, scene_end) in enumerate(scene_list):
        current_session.clip_segments[index] = Segment(current_session.clip.filepath, scene_start.seconds, scene_end.seconds, scene_end.seconds - scene_start.seconds)

