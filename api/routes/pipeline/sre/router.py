from fastapi import APIRouter

from routes.pipeline.sre.session.handler import router as session_handler
from routes.pipeline.sre.input.handler import router as input_handler
from routes.pipeline.sre.segmentation.handler import router as segmentation_handler

router = APIRouter(prefix="/sre")

desc = {
    "id": 1,
    "title": "Shorts Reverse Engineering",
    "theme": {
        "format": "bg-linear-to-br",
        "from": "from-gray-200",
        "to": "to-red-500",
        "shadow": "shadow-red-500/20"
    },
    "status": "PROTOTYPE" # later maybe ONLINE or OPERATIONAL
}

router.include_router(session_handler)

router.include_router(input_handler)

router.include_router(segmentation_handler)