from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.inspection import (
    InspectionCreate,
    InspectionUpdate,
    InspectionResponse,
    InspectionTypeCreate,
    InspectionTypeResponse,
    ChecklistCreate,
    ChecklistResponse,
)

from app.services import inspection_service


router = APIRouter(
    prefix="/inspections",
    tags=["Inspections"]
)


# -------------------------
# Inspection Types
# -------------------------

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
    response_model=List[InspectionTypeResponse]
)
def get_inspection_types(
    db: Session = Depends(get_db)
):

    return inspection_service.get_inspection_types(
        db
    )


# -------------------------
# Checklists
# -------------------------

@router.post(
    "/checklists",
    response_model=ChecklistResponse
)
def create_checklist(
    data: ChecklistCreate,
    db: Session = Depends(get_db)
):

    return inspection_service.create_checklist(
        db,
        data
    )


@router.get(
    "/checklists",
    response_model=List[ChecklistResponse]
)
def get_checklists(
    db: Session = Depends(get_db)
):

    return inspection_service.get_checklists(
        db
    )


# -------------------------
# Inspections
# -------------------------

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

    return inspection_service.get_inspections(
        db
    )


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