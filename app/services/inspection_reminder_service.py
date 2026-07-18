from sqlalchemy.orm import Session

from app.db.models.inspection_reminder import InspectionReminder


def get_reminders(
    db: Session
):

    return (
        db.query(
            InspectionReminder
        )
        .all()
    )
