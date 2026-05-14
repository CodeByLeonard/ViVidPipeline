from pathlib import Path
import shutil

SESSION = Path("./sessions/sre")

ARTIFACTS = SESSION / "artifacts"
MATCHES = ARTIFACTS / "matches"
REMATCHES = ARTIFACTS / "rematches"
SUPER_SEGMENTS = ARTIFACTS / "super_segments"

INPUT = SESSION / "input"
OUTPUT = SESSION / "output"
RECONSTRUCTION = SESSION / "reconstruction"

SEGMENTATION = SESSION / "segmentation"
CLIP_SEGMENTS = SEGMENTATION / "clip_segments"

WORKING = SESSION / "working"
EXTRACTION = WORKING / "extraction"

def initialize_workspace():
    reset_workspace()
    SESSION.mkdir(exist_ok=True)

    ARTIFACTS.mkdir(exist_ok=True)
    MATCHES.mkdir(exist_ok=True)
    REMATCHES.mkdir(exist_ok=True)
    SUPER_SEGMENTS.mkdir(exist_ok=True)

    INPUT.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)
    RECONSTRUCTION.mkdir(exist_ok=True)

    SEGMENTATION.mkdir(exist_ok=True)
    CLIP_SEGMENTS.mkdir(exist_ok=True)

    WORKING.mkdir(exist_ok=True)
    EXTRACTION.mkdir(exist_ok=True)

def reset_workspace():
    if SESSION.exists(): shutil.rmtree(SESSION)