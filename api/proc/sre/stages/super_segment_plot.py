from proc.sre.stages.source import load_source
from proc.sre.stages.super_segments import load_super_segments, SuperSegmentModel
from proc.sre.paths import SessionSRE
import matplotlib.pyplot as plt
import numpy as np

def plot_super_segment(super_segment: SuperSegmentModel):
    fig, axes = plt.subplots(3, 1, figsize=(18, 10))

    original_start = super_segment.matches[0].start
    original_end = super_segment.matches[-1].end
    clip_start = super_segment.matches[0].clip_start
    clip_end = super_segment.matches[-1].clip_end

    clip_waveform = np.load(SessionSRE.SOURCE.CLIP_WAVEFORM_NPY)
    clip_times = np.linspace(0, load_source().scope.duration, len(clip_waveform))
    axes[0].plot(clip_times, clip_waveform)
    axes[0].set_title("Full Clip Timeline")
    axes[0].axvspan(clip_start, clip_end, alpha=0.3)

    zoomed_waveform = clip_waveform[int(clip_start*16000):int(clip_end*16000)]
    zoomed_times = np.linspace(clip_start, clip_end, len(zoomed_waveform))
    axes[1].plot(zoomed_times, zoomed_waveform)
    axes[1].set_title("Zoomed Clip Timeline")

    scope_waveform = np.load(SessionSRE.SOURCE.SCOPE_WAVEFORM_NPY)
    super_waveform = scope_waveform[int(original_start * 16000):int(original_end * 16000)]
    super_times = np.linspace(original_start, original_end, len(super_waveform))
    axes[2].plot(super_times, super_waveform)
    axes[2].set_title("Super Segment Spectrogram")

    fig.tight_layout()
    return fig


def super_segments_status():
    super_segments = load_super_segments().super_segments
    scope_waveform = np.load(SessionSRE.SOURCE.SCOPE_WAVEFORM_NPY)
    clip_waveform = np.load(SessionSRE.SOURCE.CLIP_WAVEFORM_NPY)

    def plot_separate():
        for index, super_segment in enumerate(super_segments):
            # super_segment.print()
            fig = plot_super_segment(super_segment)
            fig.savefig(SessionSRE.MATCHER.SUPER_SEGMENTS / f"super_segment_{index}.png", dpi=300)

    def plot_together():
        waveforms = []

        for index, super_segment in enumerate(super_segments):
            start = super_segment.matches[0].start
            end = super_segment.matches[-1].end
            super_waveform = scope_waveform[int(start*16000):int(end*16000)]
            waveforms.append(super_waveform)

        waveform = np.concatenate(waveforms)
        times = np.linspace(0, load_source().clip.duration, len(waveform))


        fig, axes = plt.subplots(2, 1, figsize=(20, 8))

        clip_times = np.linspace(0, load_source().clip.duration, len(clip_waveform))
        axes[0].plot(clip_times, clip_waveform)
        axes[0].set_title("Original Clip Waveform")
        axes[0].set_xlim(0, load_source().clip.duration)

        axes[1].plot(times, waveform)
        axes[1].set_title("Reconstructed Super Segment Waveform")
        axes[1].set_xlim(0, load_source().clip.duration)


        fig.tight_layout()
        fig.savefig(SessionSRE.MATCHER.SUPER_SEGMENTS / "reconstruction_compare.png", dpi=300)
        plt.close(fig)

    plot_separate()
    plot_together()
