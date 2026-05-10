from fastapi import APIRouter

from routes.pipeline.reconstruct.handler import router as reconstruct_router

router = APIRouter(prefix="/pipeline")
router.include_router(reconstruct_router)
