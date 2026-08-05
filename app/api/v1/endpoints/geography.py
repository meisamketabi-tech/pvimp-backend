from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.geographic_area import GeographicArea
from app.schemas.geography import (
    GeographicAreaCreate,
    GeographicAreaUpdate,
    GeographicAreaResponse,
)


router = APIRouter(
    prefix="/geography",
    tags=["Geography"]
)


@router.get("/", response_model=list[GeographicAreaResponse])
def get_areas(
    db: Session = Depends(get_db)
):
    return db.query(GeographicArea).all()


@router.get("/{area_id}", response_model=GeographicAreaResponse)
def get_area(
    area_id: int,
    db: Session = Depends(get_db)
):
    area = db.query(GeographicArea).filter(
        GeographicArea.id == area_id
    ).first()

    if not area:
        raise HTTPException(
            status_code=404,
            detail="Geographic area not found"
        )

    return area


@router.post("/", response_model=GeographicAreaResponse)
def create_area(
    data: GeographicAreaCreate,
    db: Session = Depends(get_db)
):
    area = GeographicArea(
        **data.model_dump()
    )

    db.add(area)
    db.commit()
    db.refresh(area)

    return area


@router.put("/{area_id}", response_model=GeographicAreaResponse)
def update_area(
    area_id: int,
    data: GeographicAreaUpdate,
    db: Session = Depends(get_db)
):
    area = db.query(GeographicArea).filter(
        GeographicArea.id == area_id
    ).first()

    if not area:
        raise HTTPException(
            status_code=404,
            detail="Geographic area not found"
        )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(area, key, value)

    db.commit()
    db.refresh(area)

    return area


@router.delete("/{area_id}")
def delete_area(
    area_id: int,
    db: Session = Depends(get_db)
):
    area = db.query(GeographicArea).filter(
        GeographicArea.id == area_id
    ).first()

    if not area:
        raise HTTPException(
            status_code=404,
            detail="Geographic area not found"
        )

    db.delete(area)
    db.commit()

    return {
        "message": "Deleted successfully"
    }