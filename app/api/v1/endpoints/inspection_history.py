from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.inspection_history_service import (
    get_history
)


router = APIRouter(
    prefix="/inspection-history",
    tags=["Inspection History"]
)


@router.get(
    "/{inspection_id}"
)
def list_history(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    return get_history(
        db,
        inspection_id
    )