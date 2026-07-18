from sqlalchemy.orm import Session

from app.db.models.inspection_queue import InspectionQueue


def get_queue(
    db: Session
):

    return (
        db.query(
            InspectionQueue
        )
        .all()
    )
