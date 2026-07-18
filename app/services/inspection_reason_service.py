from sqlalchemy.orm import Session

from app.db.models.inspection_reason import InspectionReason


def get_reasons(
    db: Session
):

    return (
        db.query(
            InspectionReason
        )
        .all()
    )
