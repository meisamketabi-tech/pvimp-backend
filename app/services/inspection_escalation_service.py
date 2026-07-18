from sqlalchemy.orm import Session

from app.db.models.inspection_escalation import InspectionEscalation


def get_escalations(
    db: Session
):

    return (
        db.query(
            InspectionEscalation
        )
        .all()
    )
