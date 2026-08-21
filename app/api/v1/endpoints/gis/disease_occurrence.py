
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.db.models.gis_disease_occurrence import (
    GISDiseaseOccurrence
)

from app.schemas.gis.disease_occurrence import (
    DiseaseOccurrenceCreate,
    DiseaseOccurrenceResponse
)


router = APIRouter(
    prefix="/gis/disease-occurrences",
    tags=["GIS Disease Occurrences"]
)


@router.get(
    "/",
    response_model=list[DiseaseOccurrenceResponse]
)
def list_items(
    db: Session = Depends(get_db)
):
    return db.query(
        GISDiseaseOccurrence
    ).all()



@router.post(
    "/",
    response_model=DiseaseOccurrenceResponse
)
def create_item(
    data: DiseaseOccurrenceCreate,
    db: Session = Depends(get_db)
):

    item = GISDiseaseOccurrence(
        **data.model_dump()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item
