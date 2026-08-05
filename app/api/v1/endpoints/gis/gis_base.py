from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.db.models.gis_epidemiology_unit_type import (
    GISEpidemiologyUnitType
)

from app.db.models.gis_province import (
    GISProvince
)

from app.db.models.gis_county import (
    GISCounty
)


router = APIRouter(
    prefix="/gis",
    tags=["GIS Base"]
)



@router.get("/unit-types")
def get_unit_types(
    db: Session = Depends(get_db)
):

    return (
        db.query(GISEpidemiologyUnitType)
        .all()
    )



@router.get("/provinces")
def get_provinces(
    db: Session = Depends(get_db)
):

    return (
        db.query(GISProvince)
        .all()
    )



@router.get("/counties")
def get_counties(
    db: Session = Depends(get_db)
):

    return (
        db.query(GISCounty)
        .all()
    )