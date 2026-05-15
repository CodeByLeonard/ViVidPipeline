from pathlib import Path
import shutil

_SESSION_ROOT = Path("./sessions/sre")
class SessionSRE:
    ROOT = Path("./sessions/sre")
    SESSION_JSON = ROOT / "session.json"

    class ARTIFACTS:
        ROOT = _SESSION_ROOT / "artifacts"
        MATCHES = ROOT / "matches"
        REMATCHES = ROOT / "rematches"
        SUPER_SEGMENTS = ROOT / "super_segments"

    class INPUT:
        ROOT = _SESSION_ROOT / "input"

    class OUTPUT:
        ROOT = _SESSION_ROOT / "output"

    class RECONSTRUCTION:
        ROOT = _SESSION_ROOT / "reconstruction"

    class SEGMENTATION:
        ROOT = _SESSION_ROOT / "segmentation"
        CLIP_SEGMENTS = ROOT / "clip_segments"
        VIDEO_SEGMENTS_JSON = ROOT / "video_segments.json"
        SUPER_SEGMENTS_JSON = ROOT / "super_segments.json"
        SCOPE_JSON = ROOT / "scope.json"
        MATCHES_JSON = ROOT / "matches.json"

    class EXTRACTION:
        ROOT = _SESSION_ROOT / "extraction"
        ORIGINAL_MP3 = ROOT / "original.mp3"
        CLIP_MP3 = ROOT / "clip.mp3"

    DIRECTORIES = [
        ROOT,
        ARTIFACTS.ROOT,
        ARTIFACTS.MATCHES,
        ARTIFACTS.REMATCHES,
        ARTIFACTS.SUPER_SEGMENTS,
        INPUT.ROOT,
        OUTPUT.ROOT,
        RECONSTRUCTION.ROOT,
        SEGMENTATION.ROOT,
        SEGMENTATION.CLIP_SEGMENTS,
        EXTRACTION.ROOT,
    ]

def reset_workspace():
    if SessionSRE.ROOT.exists(): shutil.rmtree(SessionSRE.ROOT)

def mkdirs(directories: list[Path]):
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def initialize_workspace():
    reset_workspace()
    mkdirs(SessionSRE.DIRECTORIES)