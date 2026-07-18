from sqlalchemy.orm import Session

from app.db.models.inspection_correction import InspectionCorrection


def get_corrections(
    db: Session
):

    return (
        db.query(
            InspectionCorrection
        )
        .all()
    )
