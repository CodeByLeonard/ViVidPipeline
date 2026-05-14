import subprocess
from pathlib import Path

def rebuild_original(super_segments, scope, original_mono_filepath):
    segment_paths = []
    for index, super_segment in enumerate(super_segments):
        real_duration = super_segment.duration()
        target_duration = super_segment.corrected_duration()
        speed_factor = real_duration / target_duration

        seg_audio_path = f"sessions/sre/reconstruction/seg_{index}.mp3"
        segment_paths.append(seg_audio_path)
        source_start = scope.scope_to_source_time(super_segment.start())
        source_end = scope.scope_to_source_time(super_segment.end())
        command = [
            "ffmpeg", "-y",
            "-ss", str(source_start),
            "-to", str(source_end),

            "-i", f"{original_mono_filepath}",
            "-af", f"atempo={speed_factor}",
            "-c:a", "libmp3lame", seg_audio_path
        ]
        subprocess.run(command, check=True, capture_output=True)

    concat_list_path = "sessions/sre/reconstruction/concat.txt"
    with open(concat_list_path, "w") as f:
        for segment_path in segment_paths:
            absolute_path = Path(segment_path).resolve()
            f.write(f"file '{absolute_path}'\n")
    reconstructed_output = "sessions/sre/reconstruction/reconstructed.mp3"
    concat_command = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c:a", "libmp3lame",
        reconstructed_output
    ]
    subprocess.run(concat_command, check=True, capture_output=True)
    print(f"[REBUILD] Created: {reconstructed_output}")