from sqlalchemy.orm import Session

from app.db.models.inspection_action import (
    InspectionAction
)


def add_action(
    db: Session,
    inspection_id: int,
    action: str
):

    obj = InspectionAction(
        inspection_id=inspection_id,
        action=action
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj