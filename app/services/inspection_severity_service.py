from sqlalchemy.orm import Session

from app.db.models.inspection_severity import InspectionSeverity


def get_severities(
    db: Session
):

    return (
        db.query(
            InspectionSeverity
        )
        .all()
    )
