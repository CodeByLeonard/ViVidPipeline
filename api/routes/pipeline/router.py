from fastapi import APIRouter

from routes.pipeline.sre.router import router as sre_router
from routes.pipeline.sre.router import desc as sre_desc

router = APIRouter(prefix="/pipeline")
router.include_router(sre_router)

@router.get("/")
def read_item():
    list = {
        "sre": sre_desc,
    }
    return list
