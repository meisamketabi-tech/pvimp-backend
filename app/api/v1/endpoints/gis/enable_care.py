from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.gis_enable_care import GISEnableCare

from app.schemas.gis.enable_care import (
    GISEnableCareCreate,
    GISEnableCareResponse,
)

router = APIRouter(
    prefix="/gis/enable-cares",
    tags=["GIS Enable Care"],
)


@router.get("/", response_model=list[GISEnableCareResponse])
def list_items(
    db: Session = Depends(get_db),
):

    return db.query(GISEnableCare).all()


@router.post("/", response_model=GISEnableCareResponse)
def create_item(
    data: GISEnableCareCreate,
    db: Session = Depends(get_db),
):

    item = GISEnableCare(**data.model_dump())

    db.add(item)

    db.commit()

    db.refresh(item)

    return item
