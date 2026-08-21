from sqlalchemy.orm import Session

from app.db.models.inspection_alert import InspectionAlert


def get_alerts(
    db: Session
):

    return (
        db.query(
            InspectionAlert
        )
        .all()
    )
