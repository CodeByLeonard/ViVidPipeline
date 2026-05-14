from proc.sre.audio_matching.modules.source import AudioSource, MatcherView, Scope

import numpy as np
import matplotlib.pyplot as plt
import librosa

def cutout_waveform(waveform, start_time, end_time, sample_rate: int=16000):
    return waveform[int(start_time*sample_rate):int(end_time*sample_rate)]

def specshow(data, x_axis="time", cmap="magma"):
    return librosa.display.specshow(data, sr=AudioSource.sample_rate, x_axis=x_axis, cmap=cmap)

def plot_match(output, original: MatcherView, clip: MatcherView, timestamp_start, zoom: int):
    zoom = max(zoom, librosa.get_duration(y=clip.get_waveform(), sr=AudioSource.sample_rate) + 2)

    clip_S = clip.get_mel_spectrogram(n_mels=128)
    original_S = original.get_mel_spectrogram(n_mels=128)

    start_frame = int(timestamp_start * AudioSource.sample_rate / AudioSource.hop_length)
    clip_frames = clip_S.shape[1]
    end_frame = start_frame + clip_frames
    original_match_S = original_S[:, start_frame:end_frame]

    difference_matrix = np.abs(original_match_S - clip_S)


    plt.figure(figsize=(18, 10))

    plt.subplot(4, 1, 1)
    specshow(original_S)
    plt.title("Original Spectrogram (Full)")
    plt.axvline(timestamp_start, color="r", linewidth=2, label=f"Match @ {timestamp_start:.2f}s")
    plt.legend()

    zoom_start = max(-zoom, timestamp_start - zoom)
    zoom_end = min(librosa.get_duration(y=original.get_waveform(), sr=AudioSource.sample_rate)+zoom, timestamp_start + zoom)
    plt.subplot(4, 1, 2)
    specshow(original_S)
    plt.title("Original Spectrogram (Zoomed ±" + zoom.__str__() + "s)")
    plt.xlim(zoom_start, zoom_end)
    plt.axvline(timestamp_start, color="r", linewidth=2, label="Best Match")

    plt.subplot(4, 1, 3)
    specshow(clip_S)
    plt.title("Clip Spectrogram (Closeup)")
    plt.xlim(-zoom, zoom)
    # plt.axvline(timestamp_start, color="r", linewidth=2, label="Best Match")

    plt.subplot(4, 1, 4)
    specshow(difference_matrix, cmap="magma")
    plt.xlim(-zoom, zoom)
    plt.title("Difference Spectrogram")

    plt.tight_layout()
    plt.savefig(output, dpi=300)
    plt.close()

def plot_super_segment(super_segment, clip_source: AudioSource, original_source: Scope):
    fig, axes = plt.subplots(3, 1, figsize=(18, 10))

    start = super_segment.segments[0].start
    end = super_segment.segments[-1].end
    clip_start = super_segment.segments[0].clip_start
    clip_end = super_segment.segments[-1].clip_end

    clip_waveform = clip_source.waveform
    clip_times = np.linspace(0, clip_source.duration(), len(clip_waveform))
    axes[0].plot(clip_times, clip_waveform)
    axes[0].set_title("Full Clip Timeline")
    axes[0].axvspan(clip_start, clip_end, alpha=0.3)

    zoomed_waveform = cutout_waveform(clip_source.waveform, clip_start, clip_end)
    zoomed_times = np.linspace(clip_start, clip_end, len(zoomed_waveform))
    axes[1].plot(zoomed_times, zoomed_waveform)
    axes[1].set_title("Zoomed Clip Timeline")

    super_waveform = cutout_waveform(original_source.get_waveform(), start, end)
    super_times = np.linspace(0, original_source.duration(), len(super_waveform))
    axes[2].plot(super_times, super_waveform)
    axes[2].set_title("Super Segment Spectrogram")

    fig.tight_layout()
    return fig

def super_segments_status(super_segments, clip_source, scope):
    def plot_separate():
        for index, super_segment in enumerate(super_segments):
            super_segment.print()
            fig = plot_super_segment(super_segment, clip_source, scope)
            fig.savefig(f"sessions/sre/artifacts/super_segments/super_segment_{index}.png", dpi=300)

    def plot_together():
        waveforms = []

        for index, super_segment in enumerate(super_segments):
            start = super_segment.segments[0].start
            end = super_segment.segments[-1].end
            super_waveform = cutout_waveform(scope.get_waveform(), start, end)
            waveforms.append(super_waveform)

        waveform = np.concatenate(waveforms)
        times = np.linspace(0, clip_source.duration(), len(waveform))


        fig, axes = plt.subplots(2, 1, figsize=(20, 8))

        clip_waveform = clip_source.waveform
        clip_times = np.linspace(0, clip_source.duration(), len(clip_waveform))
        axes[0].plot(clip_times, clip_waveform)
        axes[0].set_title("Original Clip Waveform")
        axes[0].set_xlim(0, clip_source.duration())

        axes[1].plot(times, waveform)
        axes[1].set_title("Reconstructed Super Segment Waveform")
        axes[1].set_xlim(0, clip_source.duration())


        fig.tight_layout()
        fig.savefig("sessions/sre/artifacts/super_segments/reconstruction_compare.png", dpi=300)
        plt.close(fig)

    plot_separate()
    plot_together()