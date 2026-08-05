from sqlalchemy.orm import Session

from app.db.models.inspection_notification import InspectionNotification


def create_notification(
    db: Session,
    inspection_id: int,
    message: str,
):
    obj = InspectionNotification(
        inspection_id=inspection_id,
        message=message,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_notifications(
    db: Session,
    inspection_id: int,
):
    return (
        db.query(InspectionNotification)
        .filter(
            InspectionNotification.inspection_id == inspection_id
        )
        .all()
    )
