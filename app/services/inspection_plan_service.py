from sqlalchemy.orm import Session

from app.db.models.inspection_plan import InspectionPlan


def get_plans(
    db: Session
):

    return (
        db.query(
            InspectionPlan
        )
        .all()
    )
