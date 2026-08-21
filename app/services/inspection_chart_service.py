from sqlalchemy.orm import Session

from app.db.models.inspection_chart import InspectionChart


def get_charts(
    db: Session
):

    return (
        db.query(
            InspectionChart
        )
        .all()
    )
