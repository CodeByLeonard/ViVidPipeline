from proc.segmentation.extraction import initial_extraction
from proc.segmentation.matcher import get_matches
from proc.segmentation.pyscenedetect import fill_timestamps
from proc.segmentation.source import AudioSource, Scope, SuperSegment
from proc.segmentation.plot import super_segments_status
from pipelines.sre.session.session import current_session

import subprocess
from pathlib import Path


cutoff = 0.2
match_clip_duration = 2 + cutoff
end_find_duration = 1
next_find_duration = 1

def define_scope(original_filepath, clip_filepath):
    original_source = AudioSource(path=original_filepath)
    clip_source = AudioSource(path=clip_filepath)
    scope = Scope(original_source, [
        {"start": 274, "end": 300},
        {"start": 440, "end": 475},
        {"start": 1220, "end": 1252}
    ])
    return original_source, clip_source, scope

def fill_super_segments(matches, super_segments):
    current_super = []
    for segment in matches:
        current_super.append(segment)
        if not segment["back_link"]:
            super_segments.append(SuperSegment(current_super))
            current_super = []

def rebuild_original(super_segments, scope, original_mono_filepath):
    segment_paths = []
    for index, super_segment in enumerate(super_segments):
        real_duration = super_segment.duration()
        target_duration = super_segment.corrected_duration()
        speed_factor = real_duration / target_duration

        seg_audio_path = f"cache/rebuild/seg_{index}.mp3"
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

    concat_list_path = "cache/rebuild/concat.txt"
    with open(concat_list_path, "w") as f:
        for segment_path in segment_paths:
            absolute_path = Path(segment_path).resolve()
            f.write(f"file '{absolute_path}'\n")
    reconstructed_output = "cache/rebuild/reconstructed.mp3"
    concat_command = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c:a", "libmp3lame",
        reconstructed_output
    ]
    subprocess.run(concat_command, check=True, capture_output=True)
    print(f"[REBUILD] Created: {reconstructed_output}")

def build_cache():
    cache_rebuild = Path("./cache/rebuild")
    if not cache_rebuild.exists(): cache_rebuild.mkdir()
    cache_plot = Path("./cache/plot")
    if not cache_plot.exists(): cache_plot.mkdir()
    cache_plot_matches = Path("./cache/plot/matches")
    if not cache_plot_matches.exists(): cache_plot_matches.mkdir()
    cache_plot_super_segments = Path("./cache/plot/super_segments")
    if not cache_plot_super_segments.exists(): cache_plot_super_segments.mkdir()

def main():
    build_cache()

    original_video_filepath = current_session.original.filepath
    clip_video_filepath = current_session.clip.filepath
    original_mono_filepath = "./cache/original.mp3"
    clip_mono_filepath = "./cache/clip.mp3"

    initial_extraction(original_video_filepath, clip_video_filepath, original_mono_filepath, clip_mono_filepath)

    timestamps = [] #THIS IS A LIST OF scenedetect SEGMENTS
    fill_timestamps(timestamps, clip_video_filepath)

    # TODO: WITH HARDCODED SCOPE FOR NOW, REPLACE LATER
    original_source, clip_source, scope = define_scope(original_mono_filepath, clip_mono_filepath)

    matches = []
    get_matches(matches, timestamps, clip_source, scope)

    super_segments = []
    fill_super_segments(matches, super_segments)

    super_segments_status(super_segments, original_source, clip_source, scope)

    rebuild_original(super_segments, scope, original_mono_filepath)

    return super_segments.__len__()

if __name__ == "__main__":
    main()
