from sqlalchemy.orm import Session

from app.db.models.inspection_notification import (
    InspectionNotification
)


def create_notification(
    db: Session,
    inspection_id: int,
    message: str
):

    notification = InspectionNotification(
        inspection_id=inspection_id,
        message=message
    )

    db.add(notification)

    db.commit()

    db.refresh(notification)

    return notification