import json
import subprocess

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