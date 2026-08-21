
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.gis_send_sample_detail import (
    GISSendSampleDetail
)

from app.schemas.gis.send_sample_detail import (
    SendSampleDetailCreate,
    SendSampleDetailResponse,
)


router = APIRouter(
    prefix="/gis/send-sample-details",
    tags=["GIS Send Sample Details"],
)


@router.get(
    "/",
    response_model=list[SendSampleDetailResponse]
)
def list_items(
    db: Session = Depends(get_db),
):

    return (
        db.query(GISSendSampleDetail)
        .all()
    )


@router.post(
    "/",
    response_model=SendSampleDetailResponse
)
def create_item(
    data: SendSampleDetailCreate,
    db: Session = Depends(get_db),
):

    item = GISSendSampleDetail(
        **data.model_dump()
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item
