from proc.sre.audio_matching.modules.matcher import Match
from proc.sre.session.paths import SessionSRE
from pydantic import BaseModel
import json

SUPER_SEGMENT_FILEPATH = SessionSRE.SEGMENTATION.SUPER_SEGMENTS_JSON

class SuperSegmentModel(BaseModel):
    matches: list[Match]

class SuperSegmentsFile(BaseModel):
    super_segments: list[SuperSegmentModel]

def save_super_segments(file: SuperSegmentsFile):
    SUPER_SEGMENT_FILEPATH.parent.mkdir(parents=True, exist_ok=True)

    with open(SUPER_SEGMENT_FILEPATH, "w") as f:
        json.dump(file.model_dump(mode="json"), f, indent=2)

def load_super_segments() -> SuperSegmentsFile:
    if not SUPER_SEGMENT_FILEPATH.exists():
        return SuperSegmentsFile(super_segments=[])

    with open(SUPER_SEGMENT_FILEPATH, "r") as f:
        data = json.load(f)

    return SuperSegmentsFile.model_validate(data)

def fill_super_segments():
    from proc.sre.audio_matching.modules.matcher import load_matches
    matches = load_matches().matches
    super_segments: list[SuperSegmentModel] = []
    current: list[Match] = []

    for match in matches:
        current.append(match)

        if not match.back_link:
            super_segments.append(SuperSegmentModel(matches=current))
            current = []
    save_super_segments(SuperSegmentsFile(super_segments=super_segments))

# from proc.sre.audio_matching.modules.source import AudioSource, Scope
# class SuperSegment:
#     def __init__(self, segments):
#         self.segments = segments
#
#     def ignored_duration(self):
#          return sum(
#              segment.ignored_offset
#              for segment in self.segments
#          )
#
#     def get_scope(self, source: AudioSource):
#         timestamps = []
#         for segment in self.segments:
#             timestamps.append({"start": segment.start, "end": segment.end})
#         return Scope(source, timestamps)
#
#     def start(self):
#         return self.segments[0].start
#
#     def end(self):
#         return self.segments[-1].end
#
#     def duration(self):
#         return self.end() - self.start()
#
#     def corrected_duration(self):
#         return self.duration() + self.ignored_duration()
#
#     def print(self):
#         print("\n--------- SEGMENT PRINT ---------")
#         for index, segment in enumerate(self.segments):
#             print(f"Index {index}: {segment.__str__()}")
#         print("--------- SEGMENT PRINT ---------\n")