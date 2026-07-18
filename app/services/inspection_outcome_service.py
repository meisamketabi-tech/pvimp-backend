from sqlalchemy.orm import Session

from app.db.models.inspection_outcome import InspectionOutcome


def get_outcomes(
    db: Session
):

    return (
        db.query(
            InspectionOutcome
        )
        .all()
    )
