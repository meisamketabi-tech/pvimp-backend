from sqlalchemy.orm import Session

from app.db.models.inspection_schedule_rule import InspectionScheduleRule


def get_schedule_rules(
    db: Session
):

    return (
        db.query(
            InspectionScheduleRule
        )
        .all()
    )
