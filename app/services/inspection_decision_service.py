from sqlalchemy.orm import Session

from app.db.models.inspection_decision import InspectionDecision


def create_decision(
    db: Session,
    data,
):
    obj = InspectionDecision(
        **data.model_dump()
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_decisions(
    db: Session,
    inspection_id: int,
):
    return (
        db.query(InspectionDecision)
        .filter(
            InspectionDecision.inspection_id == inspection_id
        )
        .all()
    )
