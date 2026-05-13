from proc.segmentation.source import Scope, AudioView
import numpy as np
from proc.segmentation.plot import plot_match

def match(original_view: Scope, clip_view: AudioView, iteration: int, output: bool=False, step_frames: int=1):
    original_S = original_view.get_mel_spectrogram()
    clip_S = clip_view.get_mel_spectrogram()

    original_frames = original_S.shape[1]
    clip_frames = clip_S.shape[1]

    if clip_frames > original_frames:
        raise ValueError("Clip is larger than original search region!")

    best_score = float("inf")
    best_frame = 0

    clip_energy = np.sum(clip_S ** 2)

    # original.__len__() = session.original_source.get_mel_spectrogram().shape[1]
    for i in range(0, original_frames - clip_frames, step_frames):
        window = original_S[:, i:i + clip_frames]

        score = (
            np.sum(window ** 2)
            + clip_energy
            - 2 * np.sum(window * clip_S)
        )

        if score < best_score:
            best_score = score
            best_frame = i

    local_time = (
        best_frame
        * original_view.source.hop_length
        / original_view.source.sample_rate
    )
    print(f"[MATCH] Found match at relative {local_time:.2f}s")

    if output:
        output = f"cache/plot/matches/match_{iteration}.png"
        plot_match(output, original_view, clip_view, local_time, zoom=3)
        print(f"[MATCH] {iteration}: Saved: " + output)
    return local_time

def get_matches(matches, timestamps, clip_source, scope):
    for index, timestamp in enumerate(timestamps):
        clip_view = AudioView(clip_source, timestamp["start"], timestamp["end"])
        start_time = match(scope, clip_view, index, True)
        print(f"Start Time: {start_time}")
        duration = (timestamp["end"]-timestamp["start"])

        matches.append({
            "clip_start": timestamp["start"],
            "clip_end": timestamp["end"],

            "start": start_time,
            "end": start_time + duration,
            "duration": duration,
            "front_link": False,
            "back_link": False,
            "ignored_offset": 0.0,
        })
        print(f"matches addition: {matches[index]}")

        if not index == 0:
            a = matches[index-1]["end"]
            b = matches[index]["start"]
            c = np.abs(b-a)
            print(f"index: {index}")
            print("Checking neighbor for continuity...")
            print(f"Left Neighbor End Time: {a}")
            print(f"Own Start Time: {b}")
            print(f"Neighbor offset: {c}")
            if (c < 0.1):
                print("NEW FRONT LINK FOUND! THE OFFSET IS SMALLER THAN 0.1 SECONDS AND CAN BE IGNORED!")

                matches[index-1]["back_link"] = True
                matches[index]["front_link"] = True
                matches[index]["ignored_offset"] = c
        print("\n")