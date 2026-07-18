from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.inspection_decision_service import (
    create_decision
)


router = APIRouter(
    prefix="/inspection-decisions",
    tags=["Inspection Decisions"]
)


@router.post("")
def create(
    data,
    db: Session = Depends(get_db)
):

    return create_decision(
        db,
        data
    )
