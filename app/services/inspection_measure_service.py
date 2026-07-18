from sqlalchemy.orm import Session

from app.db.models.inspection_measure import InspectionMeasure


def get_measures(
    db: Session
):

    return (
        db.query(
            InspectionMeasure
        )
        .all()
    )
