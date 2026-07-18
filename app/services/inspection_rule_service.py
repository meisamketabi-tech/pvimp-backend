from sqlalchemy.orm import Session

from app.db.models.inspection_rule import InspectionRule


def get_rules(
    db: Session
):

    return (
        db.query(
            InspectionRule
        )
        .all()
    )
