from sqlalchemy.orm import Session

from app.db.models.inspection_metric import InspectionMetric


def get_metrics(
    db: Session
):

    return (
        db.query(
            InspectionMetric
        )
        .all()
    )
