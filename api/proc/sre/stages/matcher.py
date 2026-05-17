from proc.sre.stages.source import load_source
from proc.sre.stages.pyscenedetect import load_video_segments
from proc.sre.paths import SessionSRE
import matplotlib.pyplot as plt
from pydantic import BaseModel
from numpy import ndarray
import numpy as np
import librosa
import json

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

MATCHES_FILEPATH = SessionSRE.MATCHER.MATCHES_JSON

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
        iteration: int,
        search_mel: ndarray,
        query_mel: ndarray,
        start_limit: int | None = None, end_limit: int | None = None,
        sample_rate: int = 16000, hop_length: int = 512, step_frames: int = 1
):
    search_frames = search_mel.shape[1]
    query_frames = query_mel.shape[1]

    if query_frames > search_frames:
        raise ValueError("Clip is larger than original search region!")

    search_start_frame = 0
    if start_limit is not None:
        search_start_frame = int(start_limit * sample_rate / hop_length)

    search_end_frame = search_frames - query_frames
    if end_limit is not None:
        search_end_frame = int(end_limit * sample_rate / hop_length)

    search_start_frame = max(0, search_start_frame)
    search_end_frame = min(search_frames - query_frames, search_end_frame)

    if search_start_frame >= search_end_frame:
        raise ValueError("Invalid search limits")

    best_score = float("inf")
    best_frame = 0

    query_energy = np.sum(query_mel ** 2)

    for i in range(search_start_frame, search_end_frame, step_frames):
        window = search_mel[:, i:i + query_frames]
        score = (np.sum(window ** 2) + query_energy - 2 * np.sum(window * query_mel))

        if score < best_score:
            best_score = score
            best_frame = i

    local_time = (best_frame * hop_length / sample_rate)

    output_filepath = SessionSRE.MATCHER.MATCHES

    def plot_match(
            search_mel: ndarray, query_mel: ndarray, clip_segment_index: int,
            path: str, local_time: float, zoom: int = 3,
            sample_rate: int = 16000, hop_length: int = 512,
    ):
        start_frame = int(local_time * sample_rate / hop_length)
        query_frames = query_mel.shape[1]
        end_frame = start_frame + query_frames
        search_match_mel = search_mel[:, start_frame:end_frame]

        difference_matrix = np.abs(search_match_mel - query_mel)


        plt.figure(figsize=(18, 10))

        plt.subplot(4, 1, 1)
        librosa.display.specshow(search_mel, sr=sample_rate, x_axis="time", cmap="magma")
        plt.title("Search Mel Spectrogram (Full)")
        plt.axvline(local_time, color="r", linewidth=2, label=f"Match @ {local_time:.2f}s")
        plt.legend()

        zoom = max(zoom, load_video_segments().video_segments[clip_segment_index].duration + 2)

        zoom_start = max(-zoom, local_time - zoom)
        zoom_end = local_time + zoom
        plt.subplot(4, 1, 2)
        librosa.display.specshow(search_mel, sr=sample_rate, x_axis="time", cmap="magma")
        plt.title("Search Mel Spectrogram (Zoomed ±" + zoom.__str__() + "s)")
        plt.xlim(zoom_start, zoom_end)
        plt.axvline(local_time, color="r", linewidth=2, label="Best Match")

        plt.subplot(4, 1, 3)
        librosa.display.specshow(query_mel, sr=sample_rate, x_axis="time", cmap="magma")
        plt.title("Query Mel Spectrogram (Closeup)")
        plt.xlim(-zoom, zoom)
        # plt.axvline(local_time, color="r", linewidth=2, label="Best Match")

        plt.subplot(4, 1, 4)
        librosa.display.specshow(difference_matrix, sr=sample_rate, x_axis="time", cmap="magma")
        plt.xlim(-zoom, zoom)
        plt.title("Difference Spectrogram")

        plt.tight_layout()
        plt.savefig(path, dpi=300)
        plt.close()

    if True:
        output = f"{output_filepath}/match_{iteration}.png"
        plot_match(search_mel, query_mel, iteration, output, local_time, zoom=3)

    return local_time

def get_matches():
    # if not get_session().status.stage == "matching":
    #     return "Session not in MATCHING stage!"

    scope_mel = np.load(SessionSRE.SOURCE.SCOPE_MEL_NPY)
    video_segments = load_video_segments()
    matches: list[Match] = []

    for index, segment in enumerate(video_segments.video_segments):
        clip_mel = np.load(SessionSRE.SOURCE.CLIP_MEL_NPY)

        start_frame = int(segment.clip_start * 16000 / load_source().general.hop_length)
        end_frame = int(segment.clip_end * 16000 / load_source().general.hop_length)
        cut_clip_mel = clip_mel[:, start_frame:end_frame]

        start_time = match(index, scope_mel, cut_clip_mel)

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
    return load_matches()