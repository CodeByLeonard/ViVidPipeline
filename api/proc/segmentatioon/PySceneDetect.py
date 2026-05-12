from scenedetect import detect, AdaptiveDetector, split_video_ffmpeg

from routes.pipeline.sre.session.session import current_session

def get_segments():
    scene_list = detect(current_session.clip.filepath, AdaptiveDetector())
    # print(f"\n--------- SEGMENT LIST ---------")
    # for index, (scene_start, scene_end) in enumerate(scene_list):
    #     print(f"{index:2.0f}: {scene_start} — {scene_end}")
    # print(f"--------- SEGMENT LIST ---------\n")
    return scene_list