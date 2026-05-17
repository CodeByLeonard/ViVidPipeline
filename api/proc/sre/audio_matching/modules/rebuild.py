from proc.sre.stages.parameters import load_params
from proc.sre.stages.super_segments import load_super_segments
from proc.sre.paths import SessionSRE
from pathlib import Path
import subprocess

# OLD SUPER_SEGMENT CLASS INFORMATION, JUST TO BE SURE :)
# SUPER SEGMENT START = self.segments[0].start
# SUPER SEGMENT END = self.segments[-1].end
# SUPER SEGMENT DURATION = self.end() - self.start()
# IGNORED DURATION = sum(segment.ignored_offset) for segment in self.segments
# SUPER SEGMENT CORRECTED DURATION = self.duration() + self.ignored_duration()
# def get_scope(self, source: AudioSource):
#     timestamps = []
#     for segment in self.segments:
#         timestamps.append({"start": segment.start, "end": segment.end})
#     return Scope(source, timestamps)

def scope_to_source_time(scope_time: float):
    scopes = load_params().scopes
    scope_times_list = []
    for index, scope in enumerate(scopes):
        if (index == 0): scope_duration = scope.end - scope.start
        else: scope_duration = scope.end - scope.start + scope_times_list[index-1]
        scope_times_list.append(scope_duration)
        # 1: 20, 2: 40 + 20, 3: 10 + 40 + 20

    for index, scope_times in enumerate(scope_times_list):
        if scope_time <= scope_times:
            print(f"Found scope time {scope_time} in scope {index}")
            if index == 0: real_time = scope_time + scopes[index].start
            else: real_time = scope_time + scopes[index].start - scope_times_list[index-1]
            print(f"Real time is {real_time} in scope {index}")
            return real_time

def rebuild_original():
    super_segments = load_super_segments().super_segments
    original_mono_filepath = SessionSRE.EXTRACTION.ORIGINAL_MP3

    segment_paths = []
    for index, super_segment in enumerate(super_segments):
        total_ignored_offsets = 0.0
        for match in super_segment.matches:
            total_ignored_offsets += match.ignored_offset

        real_duration = super_segment.matches[0].start - super_segment.matches[-1].end
        target_duration = real_duration + total_ignored_offsets
        speed_factor = real_duration / target_duration

        seg_audio_path = SessionSRE.RECONSTRUCTION.ROOT / f"seg_{index}.mp3"
        segment_paths.append(seg_audio_path)

        source_start = scope_to_source_time(super_segment.matches[0].start)
        source_end = scope_to_source_time(super_segment.matches[-1].end)
        command = [
            "ffmpeg", "-y",
            "-ss", str(source_start),
            "-to", str(source_end),

            "-i", f"{original_mono_filepath}",
            "-af", f"atempo={speed_factor}",
            "-c:a", "libmp3lame", seg_audio_path
        ]
        subprocess.run(command, check=True, capture_output=True)

    concat_list_path = SessionSRE.RECONSTRUCTION.ROOT / "concat.txt"
    with open(concat_list_path, "w") as f:
        for segment_path in segment_paths:
            absolute_path = Path(segment_path).resolve()
            f.write(f"file '{absolute_path}'\n")
    reconstructed_output = SessionSRE.RECONSTRUCTION.ROOT / "reconstructed.mp3"
    concat_command = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c:a", "libmp3lame",
        reconstructed_output
    ]
    subprocess.run(concat_command, check=True, capture_output=True)
    print(f"[REBUILD] Created: {reconstructed_output}")