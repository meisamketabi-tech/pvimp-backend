from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.gis_spraying import (
    GISSpraying
)

from app.schemas.gis.spraying import (
    GISSprayingCreate,
    GISSprayingResponse,
)


router = APIRouter(
    prefix="/gis/spraying",
    tags=["GIS Spraying"],
)


@router.get(
    "/",
    response_model=list[GISSprayingResponse],
)
def list_all(
    db: Session = Depends(get_db),
):

    return (
        db.query(GISSpraying)
        .all()
    )


@router.post(
    "/",
    response_model=GISSprayingResponse,
)
def create(
    data: GISSprayingCreate,
    db: Session = Depends(get_db),
):

    item = GISSpraying(
        **data.model_dump()
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item