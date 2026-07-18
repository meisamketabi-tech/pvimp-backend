from sqlalchemy.orm import Session

from app.db.models.inspection_type_rule import InspectionTypeRule


def get_type_rules(
    db: Session
):

    return (
        db.query(
            InspectionTypeRule
        )
        .all()
    )
