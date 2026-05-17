from proc.sre.audio_matching.modules.rebuild import rebuild_original
from proc.sre.stages.matcher import get_matches
from proc.sre.stages.super_segment_plot import super_segments_status
from proc.sre.stages.super_segments import fill_super_segments
from proc.sre.stages.source import init_source_file, init_sources
from proc.sre.stages.pyscenedetect import clip_cut_detect
from proc.sre.stages.parameters import init_params, ParametersRequest
from proc.sre.stages.extracter import initial_extraction
from fastapi import APIRouter

router = APIRouter(prefix="/am")

# STEP-BY-STEP PROCEDURE

# MERGED WITH EXTRACTION STEP
@router.post("/params")
async def parameters_request(request: ParametersRequest):
    init_source_file()
    await init_params(request)
    initial_extraction() # return initial_extraction()
    init_sources()

# A VISUAL CHECK CAN BE BUILD IN IF PREFERABLE,
# TO CHECK THE SCOPE SET CORRECTLY

@router.get("/ccd")
async def clip_cut_detect_request():
    return clip_cut_detect()

# AFTER VISUAL CONFIRMATION, THE USER CAN CONTINUE TO MATCH

@router.get("/match")
async def match_request():
    return get_matches()

# ALL MATCH PLOTS ARE PRESENTED TO THE USER, AND HE CAN EITHER CONTINUE IF ALL IS GOOD,
# OR SELECT A FAULTY MATCH, AND SET A CUSTOM REMATCHING SCOPE. THEN REMATCH WITH NEW SCOPE!

@router.get("/match_correct")
async def match_correct_request():
    return "This function has not been implemented yet!"

@router.get("/super_segments")
async def super_segments_request():
    fill_super_segments()
    super_segments_status()

@router.get("/super_segments_correct")
async def super_segments_correct_request():
    return "This function has not been implemented yet!"

@router.get("/rebuild")
async def rebuild_request():
    rebuild_original()
# FUNCTIONS REBUILD_ORIGINAL WAS USED IN MAIN.PY FROM REBUILD.PY