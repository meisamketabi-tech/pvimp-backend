
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.gis_slaughter_disposal import (
    GISSlaughterDisposal
)

from app.schemas.gis.slaughter_disposal import (
    GISSlaughterDisposalCreate,
    GISSlaughterDisposalResponse,
)


router = APIRouter(
    prefix="/gis/slaughter-disposal",
    tags=["GIS Slaughter Disposal"],
)



@router.post(
    "/",
    response_model=GISSlaughterDisposalResponse,
)
def create(
    data: GISSlaughterDisposalCreate,
    db: Session = Depends(get_db),
):

    item = GISSlaughterDisposal(
        **data.model_dump()
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item



@router.get(
    "/",
    response_model=list[GISSlaughterDisposalResponse],
)
def list_all(
    db: Session = Depends(get_db),
):

    return (
        db.query(GISSlaughterDisposal)
        .all()
    )
