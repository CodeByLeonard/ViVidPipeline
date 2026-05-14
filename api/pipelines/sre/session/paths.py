from pathlib import Path
import shutil

SESSION = Path("./session")

ARTIFACTS = SESSION / "artifacts"
MATCHES = ARTIFACTS / "matches"
SUPER_SEGMENTS = ARTIFACTS / "super_segments"

INPUT = SESSION / "input"
OUTPUT = SESSION / "output"
RECONSTRUCTION = SESSION / "reconstruction"
SEGMENTATION = SESSION / "segmentation"

WORKING = SESSION / "working"
EXTRACTION = WORKING / "extraction"
SEGMENTS = WORKING / "segments"

def initialize_workspace():
    if SESSION.exists(): shutil.rmtree(SESSION)

    SESSION.mkdir(exist_ok=True)

    ARTIFACTS.mkdir(exist_ok=True)
    MATCHES.mkdir(exist_ok=True)
    SUPER_SEGMENTS.mkdir(exist_ok=True)

    INPUT.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)
    RECONSTRUCTION.mkdir(exist_ok=True)
    SEGMENTATION.mkdir(exist_ok=True)

    WORKING.mkdir(exist_ok=True)
    EXTRACTION.mkdir(exist_ok=True)
    SEGMENTS.mkdir(exist_ok=True)