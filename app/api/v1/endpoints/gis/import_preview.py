from fastapi import APIRouter

from app.services.gis.import_preview_service import (
    preview_excel,
)

router = APIRouter()


@router.post("/preview")
def preview(
    file_path: str,
):

    return preview_excel(file_path)
