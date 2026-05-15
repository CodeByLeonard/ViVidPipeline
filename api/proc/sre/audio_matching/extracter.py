from proc.sre.session import paths
from proc.sre.session.initialize import get_session, SessionData
import subprocess
import re

def extract():
    session_data = get_session().session_data
    if original(session_data) and clip(session_data): return True
    else: return False

def probe_original_stream(session_data: SessionData=get_session().session_data):
    language = session_data.preset.language
    probe = ["ffprobe", "-i", session_data.original.filepath]
    result = subprocess.run(probe, capture_output=True, text=True)

    stream_number = None
    for line in result.stderr.splitlines():
        if f"({language})" in line and "Audio:" in line:
            print(f"[EXTRACTION: Original] Found ({language}) track: {line.replace("  ", " ")}")
            match = re.search(r"Stream #0:(\d+)\(" + language + r"\): Audio:", line)
            if match: stream_number = match.group(1); break
    return stream_number

def original(session_data: SessionData=get_session().session_data):
    speed_preset = session_data.preset.speed
    language = session_data.preset.language
    channel = session_data.preset.channel

    stream_number = probe_original_stream(session_data)
    if stream_number is None:
        print(f"[EXTRACTION: Original] No ({language}) audio stream found.")
        return False

    ffmpeg_command = [
        "ffmpeg", "-y", "-i", session_data.original.filepath,
        "-map", f"0:{stream_number}",
        "-af", f"pan=mono|c0={channel},atempo={speed_preset}",
        "-acodec", "libmp3lame", "-q:a", "2",
        str(paths.SessionSRE.EXTRACTION.ORIGINAL_MP3)
    ]

    ffmpeg_result = subprocess.run(ffmpeg_command, capture_output=True, text=True)
    if ffmpeg_result.returncode == 0:
        print(f"[EXTRACTION: Original] SUCCESS: Extracted original in language {language}, {channel} channel, with speed {speed_preset:.2f}!")
        return True
    else:
        print(f"[Extraction: Original] FAILED: \n{ffmpeg_result.stderr}\n")
        return False

def clip(session_data: SessionData=get_session().session_data):
    ffmpeg_command = [
        "ffmpeg", "-y",
        "-i", session_data.clip.filepath,
        "-vn", "-ac", "1", "-q:a", "2",
        str(paths.SessionSRE.EXTRACTION.CLIP_MP3)
    ]

    result = subprocess.run(ffmpeg_command, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"[EXTRACTION: Clip] SUCCESS: Extracted mono track from the short!\n")
        return True
    else:
        print(f"[EXTRACTION: Clip] FAILED: \n{result.stderr}\n")
        return False
