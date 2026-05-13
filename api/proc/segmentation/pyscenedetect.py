from scenedetect import detect, AdaptiveDetector, split_video_ffmpeg

def get_segments(filepath):
    scene_list = detect(filepath, AdaptiveDetector())
    return scene_list

def split_video_segments(filepath):
    scene_list = get_segments(filepath) # was "cache/clip.mp4"
    split_video_ffmpeg("cache/clip.mp4", scene_list, "cache/segments")

def fill_timestamps(timestamps, filepath):
    scene_list = get_segments(filepath)
    for index, (scene_start, scene_end) in enumerate(scene_list):
        timestamps.append({
            "index": index,
            "start": scene_start.seconds,
            "end": scene_end.seconds,
            "duration": (scene_end.seconds - scene_start.seconds)
        })
    # print(timestamps)