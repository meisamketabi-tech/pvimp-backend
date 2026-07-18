from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_assignment import (
    InspectionAssignmentCreate,
    InspectionAssignmentResponse,
)

from app.services.inspection_assignment_service import (
    create_assignment,
    get_assignments,
)


router = APIRouter(
    prefix="/inspection-assignments",
    tags=["Inspection Assignments"]
)


@router.post(
    "",
    response_model=InspectionAssignmentResponse
)
def create(
    data: InspectionAssignmentCreate,
    db: Session = Depends(get_db)
):

    return create_assignment(
        db,
        data
    )


@router.get("")
def list_all(
    db: Session = Depends(get_db)
):

    return get_assignments(db)