import librosa.display
import librosa.feature

import matplotlib.pyplot as plt
import numpy as np

from proc.audio_engineering.source import Session, AudioView, AudioSource

def specshow(data, x_axis="time", cmap="magma"):
    return librosa.display.specshow(data, sr=AudioSource.sample_rate, x_axis=x_axis, cmap=cmap)

def plot_match(original: AudioView, clip: AudioView, timestamp_start, zoom: int):
    original_S = original.get_mel_spectrogram(n_mels=64)
    clip_S = clip.get_mel_spectrogram(n_mels=64)

    plt.figure(figsize=(18, 10))

    plt.subplot(4, 1, 1)
    specshow(original_S)
    plt.title("Original Spectrogram (Full)")
    plt.axvline(timestamp_start, color="r", linewidth=2, label=f"Match @ {timestamp_start:.2f}s")
    plt.legend()

    plt.subplot(4, 1, 2)
    specshow(clip_S)
    plt.title("Clip Spectrogram")

    zoom_start = max(0, timestamp_start - zoom)
    zoom_end = min(librosa.get_duration(y=original.get_waveform(), sr=AudioSource.sample_rate), timestamp_start + zoom)
    plt.subplot(4, 1, 3)
    specshow(original_S)
    plt.title("Original Spectrogram (Zoomed ±" + zoom.__str__() + "s)")
    plt.xlim(zoom_start, zoom_end)
    plt.axvline(timestamp_start, color="r", linewidth=2, label="Best Match")

    plt.subplot(4, 1, 4)
    specshow(clip_S)
    plt.title("Clip Spectrogram (Closeup)")
    plt.xlim(-zoom, zoom)
    # plt.axvline(timestamp_start, color="r", linewidth=2, label="Best Match")

    plt.tight_layout()
    return plt

def plot_scope(session: Session):
    original_S = session.original_source.get_mel_spectrogram(n_mels=64)
    clip_S = session.clip_source.get_mel_spectrogram()
    scope_S = session.scope.get_mel_spectrogram()

    plt.figure(figsize=(18, 10))

    plt.subplot(4, 1, 1)
    specshow(original_S)
    plt.title("Original Spectrogram (Full)")
    plt.axvline(session.scope.start, color="r", linewidth=2, label=f"Start Match @ {session.scope.start:.2f}s")
    plt.axvline(session.scope.end, color="r", linewidth=2, label=f"End Match @ {session.scope.end:.2f}s")
    plt.legend()

    plt.subplot(4, 1, 2)
    specshow(clip_S)
    plt.title("Clip Spectrogram (Full)")

    plt.subplot(4, 1, 3)
    specshow(scope_S)
    plt.title("Scope Spectrogram")

    zoom_start = session.scope.start
    zoom_end = session.scope.start + session.clip_source.duration()
    plt.subplot(4, 1, 4)
    specshow(original_S)
    plt.title("Scope Spectrogram (Closeup, Length same as Clip)")
    plt.axvline(session.scope.start, color="r", linewidth=2, label=f"Scope Start @ {session.scope.start:.2f}s")
    plt.xlim(zoom_start, zoom_end)
    plt.legend()

    plt.tight_layout()
    return plt

def plot_cuts(
        original_window, clip_window,
        difference_matrix, times, frame_diff, smoothed_diff,
        timestamp_cut_rough, timestamp_cut_exact,
        threshold, spike_threshold_addition,
        clip_duration
):
    plt.figure(figsize=(32, 16))

    plt.subplot(5, 1, 1)
    specshow(original_window)
    plt.title("Original Spectrogram (Aligned Selection)")
    plt.axvline(timestamp_cut_exact, color="g", linestyle="--")

    plt.subplot(5, 1, 2)
    specshow(clip_window)
    plt.title("Clip Spectrogram")
    plt.axvline(timestamp_cut_exact, color="g", linestyle="--")

    plt.subplot(5, 1, 3)
    specshow(difference_matrix, cmap="magma")
    plt.title("Difference Spectrogram")
    plt.axvline(timestamp_cut_exact, color="g", linestyle="--")

    plt.subplot(5, 1, 4)
    plt.plot(times, frame_diff)
    plt.title("Raw Deviation Over Time")
    plt.xlabel("Clip Time (seconds)")
    plt.xlim(0, clip_duration)
    if timestamp_cut_exact is not None:
        label = (
            f"Detected Cut @ {timestamp_cut_exact:.2f}s | "
            f"Spike +{spike_threshold_addition}"
        )
        plt.axvline(
            timestamp_cut_exact,
            color="r",
            linestyle="--",
            label=label
        )

        # Optional: horizontal exact spike threshold line
        # Rebuild approximate spike threshold around cut region
        exact_idx = np.searchsorted(times, timestamp_cut_exact)
        baseline_start = max(0, exact_idx - 10)
        baseline = np.mean(frame_diff[baseline_start:exact_idx]) if exact_idx > 0 else 0
        spike_threshold = baseline + spike_threshold_addition

        plt.axhline(
            spike_threshold,
            color="orange",
            linestyle=":",
            label=f"Spike Threshold ({spike_threshold:.2f})"
        )
    plt.legend()

    plt.subplot(5, 1, 5)
    plt.plot(times, smoothed_diff)
    plt.title("Smoothed Deviation Over Time")
    plt.xlabel("Clip Time (seconds)")
    plt.xlim(0, clip_duration)
    if timestamp_cut_rough is not None:
        label = (
            f"Detected Cut @ {timestamp_cut_rough:.2f}s | "
            f"Threshold {threshold}"
        )

        plt.axvline(
            timestamp_cut_rough,
            color="r",
            linestyle="--",
            label=label
        )
    plt.axhline(threshold, color="g", linestyle=":", label=f"Smooth Threshold ({threshold})")

    plt.legend()

    plt.tight_layout()
    return plt