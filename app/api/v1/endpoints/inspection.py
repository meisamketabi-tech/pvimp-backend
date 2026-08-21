from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection import (
    InspectionCreate,
    InspectionUpdate,
    InspectionStatusUpdate,
    InspectionResponse,
    InspectionTypeCreate,
    InspectionTypeResponse,
    ChecklistCreate,
    ChecklistResponse,
    InspectionStatusHistoryResponse,
)

from app.services import inspection_service


router = APIRouter(
    prefix="/inspections",
    tags=["Inspections"]
)


@router.post(
    "/types",
    response_model=InspectionTypeResponse
)
def create_inspection_type(
    data: InspectionTypeCreate,
    db: Session = Depends(get_db)
):
    return inspection_service.create_inspection_type(
        db,
        data
    )


@router.get(
    "/types",
    response_model=list[InspectionTypeResponse]
)
def get_inspection_types(
    db: Session = Depends(get_db)
):
    return inspection_service.get_inspection_types(db)

@router.post(
    "",
    response_model=InspectionResponse
)
def create_inspection(
    data: InspectionCreate,
    db: Session = Depends(get_db)
):
    return inspection_service.create_inspection(
        db,
        data
    )


@router.get(
    "",
    response_model=List[InspectionResponse]
)
def get_inspections(
    db: Session = Depends(get_db)
):
    return inspection_service.get_inspections(db)


@router.get(
    "/{inspection_id}",
    response_model=InspectionResponse
)
def get_inspection(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    inspection = inspection_service.get_inspection(
        db,
        inspection_id
    )

    if not inspection:
        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    return inspection


@router.put(
    "/{inspection_id}",
    response_model=InspectionResponse
)
def update_inspection(
    inspection_id: int,
    data: InspectionUpdate,
    db: Session = Depends(get_db)
):

    inspection = inspection_service.update_inspection(
        db,
        inspection_id,
        data
    )

    if not inspection:
        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    return inspection


@router.patch(
    '/{inspection_id}/status',
    response_model=InspectionResponse
)
def update_inspection_status(
    inspection_id: int,
    data: InspectionStatusUpdate,
    db: Session = Depends(get_db)
):

    inspection = inspection_service.update_inspection_status(
        db,
        inspection_id,
        data.status,
        changed_by=1,
        note=getattr(data, 'note', None)
    )

    if not inspection:
        raise HTTPException(
            status_code=404,
            detail='Inspection not found'
        )

    return inspection


@router.get(
    "/{inspection_id}/status-history",
    response_model=list[InspectionStatusHistoryResponse]
)
def get_inspection_status_history(
    inspection_id: int,
    db: Session = Depends(get_db)
):

    history = inspection_service.get_inspection_status_history(
        db,
        inspection_id
    )

    return history
