from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime

from app.db.session import get_db

from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit

from app.services.gis.epidemiology_import import (
    import_epidemiology_units,
)

from app.schemas.gis.epidemiology_unit import (
    EpidemiologyUnitCreate,
    EpidemiologyUnitUpdate,
    EpidemiologyUnitResponse,
)

router = APIRouter(
    prefix="/gis/epidemiology-units",
    tags=["GIS Epidemiology Units"],
)


# -------------------------------------------------
# Import Excel
# -------------------------------------------------


@router.post("/import")
async def import_units(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    upload_dir = Path("uploads/gis/disease-control/epidemiology-units")

    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + file.filename

    file_path = upload_dir / filename

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    result = import_epidemiology_units(
        db,
        str(file_path),
    )

    return {
        "file": filename,
        "path": str(file_path),
        "result": result,
    }


# -------------------------------------------------
# Get all units
# -------------------------------------------------


@router.get(
    "/",
    response_model=list[EpidemiologyUnitResponse],
)
def get_units(
    db: Session = Depends(get_db),
):

    return db.query(GISEpidemiologyUnit).all()


# -------------------------------------------------
# Get one unit
# -------------------------------------------------


@router.get(
    "/{unit_id}",
    response_model=EpidemiologyUnitResponse,
)
def get_unit(
    unit_id: int,
    db: Session = Depends(get_db),
):

    unit = (
        db.query(GISEpidemiologyUnit).filter(GISEpidemiologyUnit.id == unit_id).first()
    )

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Epidemiology unit not found",
        )

    return unit


# -------------------------------------------------
# Create unit
# -------------------------------------------------


@router.post(
    "/",
    response_model=EpidemiologyUnitResponse,
)
def create_unit(
    data: EpidemiologyUnitCreate,
    db: Session = Depends(get_db),
):

    unit = GISEpidemiologyUnit(**data.model_dump())

    db.add(unit)
    db.commit()
    db.refresh(unit)

    return unit


# -------------------------------------------------
# Update unit
# -------------------------------------------------


@router.put(
    "/{unit_id}",
    response_model=EpidemiologyUnitResponse,
)
def update_unit(
    unit_id: int,
    data: EpidemiologyUnitUpdate,
    db: Session = Depends(get_db),
):

    unit = (
        db.query(GISEpidemiologyUnit).filter(GISEpidemiologyUnit.id == unit_id).first()
    )

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Epidemiology unit not found",
        )

    for key, value in data.model_dump(exclude_unset=True).items():

        setattr(
            unit,
            key,
            value,
        )

    db.commit()
    db.refresh(unit)

    return unit


# -------------------------------------------------
# Delete unit
# -------------------------------------------------


@router.delete(
    "/{unit_id}",
)
def delete_unit(
    unit_id: int,
    db: Session = Depends(get_db),
):

    unit = (
        db.query(GISEpidemiologyUnit).filter(GISEpidemiologyUnit.id == unit_id).first()
    )

    if not unit:
        raise HTTPException(
            status_code=404,
            detail="Epidemiology unit not found",
        )

    db.delete(unit)
    db.commit()

    return {"message": "Deleted successfully"}
