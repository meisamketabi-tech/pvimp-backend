from sqlalchemy.orm import Session

from app.db.models.inspection_reminder_rule import InspectionReminderRule


def get_reminder_rules(
    db: Session
):

    return (
        db.query(
            InspectionReminderRule
        )
        .all()
    )
