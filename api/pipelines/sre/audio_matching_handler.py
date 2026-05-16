from proc.sre.audio_matching.modules.matcher import get_matches
from proc.sre.audio_matching.super_segments import fill_super_segments
from proc.sre.stages.extracter import initial_extraction
from proc.sre.stages.parameters import init_params, ParametersRequest
from proc.sre.stages.pyscenedetect import clip_cut_detect
from fastapi import APIRouter

router = APIRouter(prefix="/am")

# STEP-BY-STEP PROCEDURE

# MERGED WITH EXTRACTION STEP
@router.post("/params")
async def parameters_request(request: ParametersRequest):
    await init_params(request)
    return initial_extraction()

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

# def rematch():
#     corrections = load_corrections()
#     from proc.sre.audio_matching.modules.source import set_scope
#     original_source, clip_source, scope = set_scope(original_mono_filepath, clip_mono_filepath)
#     print(f"[RE-MATCHER] Initiated Rematch! Manual Corrections:")
#     for index, correction in enumerate(corrections):
#         print(f"Correction {index}: \n{correction}")
#         get_rematches(clip_source, scope, corrections.match_corrections)
#
#     print("\n")
#     super_segments = []
#     from proc.sre.audio_matching.modules.source import fill_super_segments
#     fill_super_segments(super_segments)
#     from proc.sre.audio_matching.modules.plot import super_segments_status
#     super_segments_status(super_segments, clip_source, scope)
#     rebuild_original(super_segments, scope, original_mono_filepath)
#     return

@router.get("/super_segments")
async def super_segments_request():
    return fill_super_segments()
# MISSING HERE IS SUPER SEGMENT STATUS, WHICH PLOTS AND OUTPUTS THE SUPER SEGMENTS TO CONSOLE, LOCATED IN PLOT.PY!

@router.get("/super_segments_correct")
async def super_segments_correct_request():
    return "This function has not been implemented yet!"

@router.get("/rebuild")
async def rebuild_request():
    return "This function has not been implemented yet!"
# FUNCTIONS REBUILD_ORIGINAL WAS USED IN MAIN.PY FROM REBUILD.PY