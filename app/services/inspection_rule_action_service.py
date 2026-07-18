from sqlalchemy.orm import Session

from app.db.models.inspection_rule_action import InspectionRuleAction


def get_rule_actions(
    db: Session
):

    return (
        db.query(
            InspectionRuleAction
        )
        .all()
    )
