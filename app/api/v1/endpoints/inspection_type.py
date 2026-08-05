from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection import (
    InspectionTypeCreate,
    InspectionTypeResponse,
)

from app.services.inspection_service import (
    create_inspection_type,
    get_inspection_types,
)


router = APIRouter(
    prefix="/inspections",
    tags=["Inspection Types"]
)


@router.post(
    "/types",
    response_model=InspectionTypeResponse
)
def create(
    data: InspectionTypeCreate,
    db: Session = Depends(get_db)
):

    return create_inspection_type(
        db,
        data
    )


@router.get(
    "/types",
    response_model=List[InspectionTypeResponse]
)
def list_all(
    db: Session = Depends(get_db)
):

    return get_inspection_types(
        db
    )