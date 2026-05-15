from proc.sre.audio_matching.modules.corrections import MatchCorrectionEntry
from proc.sre.audio_matching.modules.pyscenedetect import load_video_segments
from proc.sre.audio_matching.modules.source import Scope, AudioView
from proc.sre.audio_matching.modules.plot import plot_match
from pydantic import BaseModel
import numpy as np
import json

from proc.sre.audio_matching.scope import get_scope_elements
from proc.sre.session.paths import SessionSRE

MATCHES_FILEPATH = SessionSRE.SEGMENTATION.MATCHES_JSON

class Match(BaseModel):
    index: int
    clip_start: float
    clip_end: float

    start: float
    end: float
    duration: float
    front_link: bool
    back_link: bool
    ignored_offset: float

class MatchesFile(BaseModel):
    matches: list[Match]

def save_matches(file: MatchesFile):
    MATCHES_FILEPATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MATCHES_FILEPATH, "w") as f:
        json.dump(file.model_dump(mode="json"), f, indent=2)

def load_matches() -> MatchesFile:
    if not MATCHES_FILEPATH.exists():
        raise FileNotFoundError("Matches does not exist")
    with open(MATCHES_FILEPATH, "r") as f:
        data = json.load(f)
    return MatchesFile.model_validate(data)

def match(
        original_view: Scope, clip_view: AudioView,
        iteration: int, output: bool=False, output_filepath: str=str(SessionSRE.ARTIFACTS.MATCHES), step_frames: int=1,
        start_limit: float | None = None, end_limit: float | None = None
):
    original_S = original_view.get_mel_spectrogram()
    clip_S = clip_view.get_mel_spectrogram()

    original_frames = original_S.shape[1]
    clip_frames = clip_S.shape[1]

    if clip_frames > original_frames:
        raise ValueError("Clip is larger than original search region!")

    sample_rate = original_view.source.sample_rate
    hop_length = original_view.source.hop_length

    search_start_frame = 0
    if start_limit is not None:
        search_start_frame = int(start_limit * sample_rate / hop_length)

    search_end_frame = original_frames - clip_frames
    if end_limit is not None:
        search_end_frame = int(end_limit * sample_rate / hop_length)

    search_start_frame = max(0, search_start_frame)
    search_end_frame = min(original_frames - clip_frames, search_end_frame)

    if search_start_frame >= search_end_frame:
        raise ValueError("Invalid search limits")

    best_score = float("inf")
    best_frame = 0

    clip_energy = np.sum(clip_S ** 2)

    # original.__len__() = session.original_source.get_mel_spectrogram().shape[1]
    for i in range(search_start_frame, search_end_frame, step_frames):
        window = original_S[:, i:i + clip_frames]

        score = (
            np.sum(window ** 2)
            + clip_energy
            - 2 * np.sum(window * clip_S)
        )

        if score < best_score:
            best_score = score
            best_frame = i

    local_time = (best_frame * hop_length / sample_rate)

    if output:
        output = f"{output_filepath}/match_{iteration}.png"
        plot_match(output, original_view, clip_view, local_time, zoom=3)
    return local_time

def get_matches():
    original_source, clip_source, scope = get_scope_elements()
    video_segments = load_video_segments()
    matches: list[Match] = []

    for index, segment in enumerate(video_segments.video_segments):
        clip_view = AudioView(clip_source, segment.clip_start, segment.clip_end)
        start_time = match(scope, clip_view, index, True)
        matches.append(
            Match(
                index=index,
                clip_start=segment.clip_start,
                clip_end=segment.clip_end,
                start=start_time,
                end=start_time + segment.duration,
                duration=segment.duration,
                front_link=False,
                back_link=False,
                ignored_offset=0.0
            )
        )

        print("\n")
        print(f"[MATCHER] Matching segment {index} complete.. ({index}/{len(video_segments.video_segments)-1})")
        if not index == 0:
            a = matches[index-1].end
            b = matches[index].start
            c = np.abs(b-a)
            print(f"index: {index}")
            print(f"Left Neighbor End Time: {a}")
            print(f"Own Start Time: {b}")
            print(f"Neighbor offset: {c}")
            if (c < 0.1):
                print("NEW FRONT LINK FOUND!")
                matches[index-1].back_link = True
                matches[index].front_link = True
                matches[index].ignored_offset = c
        print("\n")

    save_matches(MatchesFile(matches=matches))

def get_rematches(clip_source, scope, match_corrections: list[MatchCorrectionEntry]):
    correction = match_corrections[0]
    index = correction.match

    matches_file = load_matches()
    matches = matches_file.matches

    segment = load_video_segments().video_segments[index]
    clip_view = AudioView(clip_source, segment.clip_start, segment.clip_end)
    start_time = match(scope, clip_view, index, True, output_filepath=str(SessionSRE.ARTIFACTS.REMATCHES),
                       start_limit=match_corrections[0].start_match, end_limit=match_corrections[0].end_match)

    print("\n")
    print(f"[RE-MATCHER] Matching segment {index} complete!")
    print(f"[RE-MATCHER] Now matched to {start_time}s.")

    matches[index] = Match(
        index=index,
        clip_start=segment.clip_start,
        clip_end=segment.clip_end,
        start=start_time,
        end=start_time + segment.duration,
        duration=segment.duration,
        front_link=False,
        back_link=False,
        ignored_offset=0.0
    )

    if index > 0:
        a = matches[index - 1].end
        b = matches[index].start
        c = np.abs(b - a)

        print(f"index: {index}")
        print(f"Left Neighbor End Time: {a}")
        print(f"Own Start Time: {b}")
        print(f"Neighbor offset: {c}")
        if (c < 0.1):
            print("NEW FRONT LINK FOUND!")
            matches[index - 1].back_link = True
            matches[index].front_link = True
            matches[index].ignored_offset = c
    print("\n")
    save_matches(MatchesFile(matches=matches))