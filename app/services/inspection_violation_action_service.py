from sqlalchemy.orm import Session

from app.db.models.inspection_violation_action import InspectionViolationAction


def get_violation_actions(
    db: Session
):

    return (
        db.query(
            InspectionViolationAction
        )
        .all()
    )
