from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection import (
    InspectionResponse
)

from app.schemas.inspection_filter import (
    InspectionFilter
)

from app.services.inspection_filter_service import (
    filter_inspections
)


router = APIRouter(
    prefix="/inspection-filter",
    tags=["Inspection Filter"]
)


@router.post(
    "",
    response_model=List[InspectionResponse]
)
def filter_data(
    filters: InspectionFilter,
    db: Session = Depends(get_db)
):

    return filter_inspections(
        db,
        filters
    )