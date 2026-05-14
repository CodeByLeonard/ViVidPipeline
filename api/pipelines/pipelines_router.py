from fastapi import APIRouter

from pipelines.sre.sre_router import router as sre_router
from pipelines.sre.sre_router import description as sre_description

from pipelines.preview.preview_router import router as preview_router
from pipelines.preview.preview_router import description as preview_description

router = APIRouter(prefix="/pip")
router.include_router(sre_router)
router.include_router(preview_router)

@router.get("/")
def list_pipelines():
    return {"preview": preview_description, "sre": sre_description}

@router.get("/reset")
def reset_pipelines():
    from pipelines.preview.preview_router import clear as clear_preview
    clear_preview()
    from proc.sre.session.paths import reset_workspace
    reset_workspace()
    return {}
