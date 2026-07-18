from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_lab_result import (
    InspectionLabResultResponse
)

from app.services.inspection_lab_result_service import (
    create_result
)


router = APIRouter(
    prefix="/inspection-lab-results",
    tags=["Inspection Lab Results"]
)


@router.post("")
def create(
    data,
    db: Session = Depends(get_db)
):

    return create_result(
        db,
        data
    )
