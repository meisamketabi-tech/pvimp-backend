from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.inspection_review_service import (
    create_review
)


router = APIRouter(
    prefix="/inspection-reviews",
    tags=["Inspection Reviews"]
)


@router.post("")
def create(
    data,
    db: Session = Depends(get_db)
):

    return create_review(
        db,
        data
    )
