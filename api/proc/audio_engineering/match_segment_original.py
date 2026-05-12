from routes.pipeline.sre.session.session import current_session
import numpy as np
from proc.audio_engineering.source import AudioView
from proc.audio_engineering.plot import plot_match
from proc.audio_engineering.preset import cutoff, start_find_duration


def match_segment_original():
    print("audio_engineering initiated")
    original_view = AudioView(current_session.original.filepath, 0, 2400)
    clip_view = AudioView(current_session.clip.filepath, current_session.clip_segments[0].start_time, current_session.clip_segments[0].end_time)
    timestamp_start = match(original_view, clip_view, iteration=1, output=False)
    print(f"\n[*] Start Timestamp set at {(timestamp_start / 60):.1f}m {(timestamp_start % 60):.4f}\n")

def match(original_view: AudioView, clip_view: AudioView, iteration: int, output: bool=False, step_frames: int=1):
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

    best_time_absolute = original_view.start + local_time
    print(f"[MATCH] Found match at relative {local_time:.2f}s and absolute {best_time_absolute:.2f}s")

    if output:
        output = f"tmp/match_{iteration}.png"
        plot_match(original_view, clip_view, local_time, zoom=10).savefig(output, dpi=300)
        print(f"[MATCH] {iteration}: Saved: " + output)
    return local_time