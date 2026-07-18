from sqlalchemy.orm import Session

from app.db.models.inspection_history_note import InspectionHistoryNote


def get_history_notes(
    db: Session
):

    return (
        db.query(
            InspectionHistoryNote
        )
        .all()
    )
