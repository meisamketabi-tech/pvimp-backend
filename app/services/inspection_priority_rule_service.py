from sqlalchemy.orm import Session

from app.db.models.inspection_priority_rule import InspectionPriorityRule


def get_priority_rules(
    db: Session
):

    return (
        db.query(
            InspectionPriorityRule
        )
        .all()
    )
