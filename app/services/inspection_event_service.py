from sqlalchemy.orm import Session

from app.db.models.inspection_event import InspectionEvent


def get_events(
    db: Session
):

    return (
        db.query(
            InspectionEvent
        )
        .all()
    )
