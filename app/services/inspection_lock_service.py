from sqlalchemy.orm import Session

from app.db.models.inspection_lock import InspectionLock


def create_lock(
    db: Session,
    inspection_id: int,
    user_id: int
):

    obj = InspectionLock(
        inspection_id=inspection_id,
        locked_by=user_id
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
