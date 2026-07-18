from sqlalchemy.orm import Session

from app.db.models.inspection_indicator import InspectionIndicator


def get_indicators(
    db: Session
):

    return (
        db.query(
            InspectionIndicator
        )
        .all()
    )
