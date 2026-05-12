from fastapi import APIRouter

from routes.pipeline.reconstruct.handler import router as reconstruct_router
from routes.pipeline.session.handler import router as session_router

router = APIRouter(prefix="/pipeline")

router.include_router(reconstruct_router)
router.include_router(session_router)
