from sqlalchemy.orm import Session

from app.db.models.inspection_followup import InspectionFollowUp


def create_followup(
    db: Session,
    data,
):
    obj = InspectionFollowUp(
        **data.model_dump()
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_followups(
    db: Session,
    inspection_id: int,
):
    return (
        db.query(InspectionFollowUp)
        .filter(
            InspectionFollowUp.inspection_id == inspection_id
        )
        .all()
    )
