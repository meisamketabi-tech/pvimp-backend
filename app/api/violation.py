from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.violation import Violation


router = APIRouter(
    prefix="/violations",
    tags=["Violations"]
)


@router.post("/")
def create_violation(
    data: dict,
    db: Session = Depends(get_db)
):

    obj = Violation(
        **data
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj



@router.get("/")
def list_violations(
    db: Session = Depends(get_db)
):

    return db.query(
        Violation
    ).order_by(
        Violation.id.desc()
    ).all()



@router.get("/unit/{id}")
def unit_violations(
    id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        Violation
    ).filter(
        Violation.inspection_id == id
    ).all()