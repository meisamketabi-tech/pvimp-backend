from sqlalchemy.orm import Session

from app.db.models.inspection_history import (
    InspectionHistory
)


def add_history(
    db: Session,
    inspection_id: int,
    action: str
):

    history = InspectionHistory(
        inspection_id=inspection_id,
        action=action
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return history



def get_history(
    db: Session,
    inspection_id: int
):

    return (
        db.query(
            InspectionHistory
        )
        .filter(
            InspectionHistory.inspection_id ==
            inspection_id
        )
        .all()
    )