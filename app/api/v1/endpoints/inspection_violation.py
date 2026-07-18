from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_violation import (
    InspectionViolationCreate,
    InspectionViolationResponse,
)

from app.services.inspection_violation_service import (
    create_violation,
    get_violations,
)


router = APIRouter(
    prefix="/inspection-violations",
    tags=["Inspection Violations"]
)


@router.post(
    "",
    response_model=InspectionViolationResponse
)
def create(
    data: InspectionViolationCreate,
    db: Session = Depends(get_db)
):

    return create_violation(
        db,
        data
    )


@router.get(
    "/{inspection_id}",
    response_model=List[InspectionViolationResponse]
)
def list_all(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    return get_violations(
        db,
        inspection_id
    )