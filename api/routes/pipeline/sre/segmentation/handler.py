from fastapi import APIRouter

from proc.segmentation.pyscenedetect import get_segments
from routes.pipeline.sre.session.session import current_session
from routes.pipeline.sre.segmentation.segment import Segment

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

    from proc.segmentation.main import main
    super_segment_length = main()

    return {"segments": current_session.clip_segments}

def divide_clip():
    scene_list = get_segments(current_session.clip.filepath)
    for index, (scene_start, scene_end) in enumerate(scene_list):
        current_session.clip_segments[index] = Segment(current_session.clip.filepath, scene_start.seconds, scene_end.seconds, scene_end.seconds - scene_start.seconds)

@router.get("/test")
async def test():
    from routes.pipeline.sre.session.handler import reset
    reset()

    from routes.pipeline.sre.input.handler import youtube
    youtube("Eon2EqOfGbs")

    import shutil
    shutil.copy("routes/pipeline/sre/segmentation/original.mkv", "cache/original.mkv")
    from routes.pipeline.sre.input.original import Original
    original = Original("cache/original.mkv")
    current_session.original = original

    from routes.pipeline.sre.session.handler import initialize
    await initialize()

    from proc.segmentation.main import main
    super_segment_length = main()
    return super_segment_length
