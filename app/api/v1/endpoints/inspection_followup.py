from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_followup import (
    InspectionFollowUpCreate,
    InspectionFollowUpResponse,
)

from app.services.inspection_followup_service import (
    create_followup,
    get_followups,
)


router = APIRouter(
    prefix="/inspection-followups",
    tags=["Inspection Followups"]
)


@router.post(
    "",
    response_model=InspectionFollowUpResponse
)
def create(
    data: InspectionFollowUpCreate,
    db: Session = Depends(get_db)
):

    return create_followup(
        db,
        data
    )


@router.get(
    "/{inspection_id}",
    response_model=List[InspectionFollowUpResponse]
)
def list_all(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    return get_followups(
        db,
        inspection_id
    )