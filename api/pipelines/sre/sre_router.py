from fastapi import APIRouter

from pipelines.sre.session.handler import router as session_handler
from pipelines.sre.input.handler import router as input_handler
from pipelines.sre.segmentation.handler import router as segmentation_handler

router = APIRouter(prefix="/sre")

@router.get("/")
def list_pipelines():
    return description

description = {
    "id": 1,
    "title": "Shorts Reverse Engineering",
    "theme": {
        "from": "from-gray-200",
        "to": "to-red-500",
        "shadow": "shadow-red-500/20"
    },
    "status": "PROTOTYPE" # later maybe ONLINE or OPERATIONAL
}

router.include_router(session_handler)

# router.include_router(input_handler)

# router.include_router(segmentation_handler)