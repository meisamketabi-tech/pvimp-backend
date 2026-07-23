from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.inspection import Inspection


router = APIRouter(
    prefix="/inspections",
    tags=["Inspections"]
)


@router.post("/")
def create_inspection(
    data: dict,
    db: Session = Depends(get_db)
):

    obj = Inspection(
        **data
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


@router.get("/")
def list_inspections(
    db: Session = Depends(get_db)
):

    return db.query(
        Inspection
    ).order_by(
        Inspection.id.desc()
    ).all()