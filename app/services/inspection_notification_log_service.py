from sqlalchemy.orm import Session

from app.db.models.inspection_notification_log import InspectionNotificationLog


def get_notification_logs(
    db: Session
):

    return (
        db.query(
            InspectionNotificationLog
        )
        .all()
    )
