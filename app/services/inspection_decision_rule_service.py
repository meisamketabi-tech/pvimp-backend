from sqlalchemy.orm import Session

from app.db.models.inspection_decision_rule import InspectionDecisionRule


def get_decision_rules(
    db: Session
):

    return (
        db.query(
            InspectionDecisionRule
        )
        .all()
    )
