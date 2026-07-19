from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_assignment import (
    InspectionAssignmentCreate,
    InspectionAssignmentResponse,
)

from app.services.inspection_assignment_service import (
    create_assignment,
    get_assignments,
    get_inspection_assignments,
    unassign_inspection,
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

    assignment = create_assignment(
        db,
        data,
        assigned_by=1
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    return assignment



@router.get(
    "",
    response_model=List[InspectionAssignmentResponse]
)
def list_all(
    db: Session = Depends(get_db)
):

    return get_assignments(db)



@router.get(
    "/inspection/{inspection_id}",
    response_model=List[InspectionAssignmentResponse]
)
def list_by_inspection(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    return get_inspection_assignments(
        db,
        inspection_id
    )



@router.delete(
    "/{assignment_id}",
    response_model=InspectionAssignmentResponse
)
def unassign(
    assignment_id: int,
    db: Session = Depends(get_db)
):

    assignment = unassign_inspection(
        db,
        assignment_id
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    return assignment
