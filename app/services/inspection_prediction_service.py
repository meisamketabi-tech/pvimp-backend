from sqlalchemy.orm import Session

from app.db.models.inspection_prediction import InspectionPrediction


def get_predictions(
    db: Session
):

    return (
        db.query(
            InspectionPrediction
        )
        .all()
    )
