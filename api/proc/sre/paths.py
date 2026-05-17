from pathlib import Path
import shutil

_SESSION_ROOT = Path("./sessions/sre")
class SessionSRE:
    ROOT = Path("./sessions/sre")
    SESSION_JSON = ROOT / "session.json"

    class EXTRACTION:
        ROOT = _SESSION_ROOT / "extraction"
        ORIGINAL_MP3 = ROOT / "original.mp3"
        CLIP_MP3 = ROOT / "clip.mp3"
        PARAMETERS_JSON = ROOT / "parameters.json"

    class MATCHER:
        ROOT = _SESSION_ROOT / "matcher"
        MATCHES = ROOT / "plot_matches"
        REMATCHES = ROOT / "plot_rematches"
        SUPER_SEGMENTS = ROOT / "plot_super_segments"
        MATCHES_JSON = ROOT / "matches.json"
        SUPER_SEGMENTS_JSON = ROOT / "super_segments.json"

    class INPUT:
        ROOT = _SESSION_ROOT / "input"
        CLIP = ROOT / "clip.mp4"
        ORIGINAL = ROOT / "original.mkv"

    class OUTPUT:
        ROOT = _SESSION_ROOT / "output"

    class RECONSTRUCTION:
        ROOT = _SESSION_ROOT / "reconstruction"

    class SEGMENTATION:
        ROOT = _SESSION_ROOT / "segmentation"
        CLIP_SEGMENTS = ROOT / "clip_segments"
        VIDEO_SEGMENTS_JSON = ROOT / "clip_segments.json"

    class SOURCE:
        ROOT = _SESSION_ROOT / "source"
        SOURCE_JSON = ROOT / "source.json"

        ORIGINAL = ROOT / "original"
        ORIGINAL_WAVEFORM_NPY = ORIGINAL / "waveform.npy"
        ORIGINAL_MEL_NPY = ORIGINAL / "mel.npy"
        ORIGINAL_METADATA_JSON = ORIGINAL / "metadata.json"

        CLIP = ROOT / "clip"
        CLIP_WAVEFORM_NPY = CLIP / "waveform.npy"
        CLIP_MEL_NPY = CLIP / "mel.npy"
        CLIP_METADATA_JSON = CLIP / "metadata.json"

        SCOPE = ROOT / "scope"
        SCOPE_WAVEFORM_NPY = SCOPE / "waveform.npy"
        SCOPE_MEL_NPY = SCOPE / "mel.npy"
        SCOPE_METADATA_JSON = SCOPE / "metadata.json"

    DIRECTORIES = [
        ROOT,
        MATCHER.ROOT,
        MATCHER.MATCHES,
        MATCHER.REMATCHES,
        MATCHER.SUPER_SEGMENTS,
        INPUT.ROOT,
        OUTPUT.ROOT,
        RECONSTRUCTION.ROOT,
        SEGMENTATION.ROOT,
        SEGMENTATION.CLIP_SEGMENTS,
        EXTRACTION.ROOT,
        SOURCE.ROOT,
        SOURCE.ORIGINAL,
        SOURCE.CLIP,
        SOURCE.SCOPE,
    ]

def reset_workspace():
    if SessionSRE.ROOT.exists(): shutil.rmtree(SessionSRE.ROOT)

def mkdirs(directories: list[Path]):
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def initialize_workspace():
    reset_workspace()
    mkdirs(SessionSRE.DIRECTORIES)