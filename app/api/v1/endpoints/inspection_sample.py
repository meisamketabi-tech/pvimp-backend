from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection_sample import (
    InspectionSampleCreate,
    InspectionSampleResponse,
)

from app.services.inspection_sample_service import create_sample


router = APIRouter(
    prefix="/inspection-samples",
    tags=["Inspection Samples"]
)


@router.post(
    "",
    response_model=InspectionSampleResponse
)
def create(
    data: InspectionSampleCreate,
    db: Session = Depends(get_db)
):

    return create_sample(
        db,
        data
    )
