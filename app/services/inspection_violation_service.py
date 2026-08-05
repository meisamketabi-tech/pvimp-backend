from sqlalchemy.orm import Session

from app.db.models.inspection_violation import InspectionViolation


def create_violation(
    db: Session,
    data,
):
    obj = InspectionViolation(
        **data.model_dump()
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_violations(
    db: Session,
    inspection_id: int,
):
    return (
        db.query(InspectionViolation)
        .filter(
            InspectionViolation.inspection_id == inspection_id
        )
        .all()
    )
