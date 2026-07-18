from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.inspection_score_service import (
    calculate_score
)


router = APIRouter(
    prefix="/inspection-scores",
    tags=["Inspection Scores"]
)


@router.post(
    "/{inspection_id}"
)
def create_score(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    return calculate_score(
        db,
        inspection_id
    )