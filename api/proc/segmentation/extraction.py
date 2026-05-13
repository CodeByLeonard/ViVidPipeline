import subprocess
import re

def initial_extraction(original_video_filepath, clip_video_filepath, original_mono_filepath, clip_mono_filepath):
    original_success = original(original_video_filepath, original_mono_filepath)
    clip_success = clip(clip_video_filepath, clip_mono_filepath)
    if original_success and clip_success: return True
    else: return False

def original(original_video_filepath, original_mono_filepath):
    speed_preset = 0.97274376 * 0.99  # = 0.9630163224
    language = "eng"
    channel = "FC"

    probe = ["ffprobe", "-i", original_video_filepath]
    result = subprocess.run(probe, capture_output=True, text=True)

    stream_number = None
    for line in result.stderr.splitlines():
        if f"({language})" in line and "Audio:" in line:
            print(f"[EXTRACTION] Found ({language}) track: {line}")
            match = re.search(r"Stream #0:(\d+)\(" + language + r"\): Audio:", line)
            if match: stream_number = match.group(1); break

    if stream_number is None:
        print(f"[EXTRACTION] No ({language}) audio stream found.")
        return False

    extract = [
        "ffmpeg", "-y", "-i", original_video_filepath,
        "-map", f"0:{stream_number}",
        "-af", f"pan=mono|c0={channel},atempo={speed_preset}",
        "-acodec", "libmp3lame", "-q:a", "2",
        original_mono_filepath
    ]
    ffmpeg_result = subprocess.run(extract, capture_output=True, text=True)

    if ffmpeg_result.returncode == 0:
        print(f"[EXTRACTION] SUCCESS: Extracted {language} {channel} channel with speed {speed_preset} to {original_mono_filepath}!\n")
        return True
    else:
        print(f"[Extraction] FAILED: \n{ffmpeg_result.stderr}\n")
        return False

def clip(clip_video_filepath, clip_mono_filepath):
    extract = ["ffmpeg", "-y", "-i", clip_video_filepath, "-vn", "-ac", "1", "-q:a", "2", clip_mono_filepath]
    result = subprocess.run(extract, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[EXTRACTION] SUCCESS: Extracted mono track from {clip_video_filepath} to {clip_mono_filepath}!\n")
        return True
    else:
        print(f"[EXTRACTION] FAILED: \n{result.stderr}\n")
        return False
