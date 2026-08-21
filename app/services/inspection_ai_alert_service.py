from sqlalchemy.orm import Session

from app.db.models.inspection_ai_alert import InspectionAIAlert


def get_ai_alerts(
    db: Session
):

    return (
        db.query(
            InspectionAIAlert
        )
        .all()
    )
