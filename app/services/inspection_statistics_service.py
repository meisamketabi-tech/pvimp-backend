from sqlalchemy.orm import Session

from app.db.models.inspection_statistics import InspectionStatistics


def get_statistics(
    db: Session
):

    return (
        db.query(
            InspectionStatistics
        )
        .all()
    )
