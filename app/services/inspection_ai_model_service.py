from sqlalchemy.orm import Session

from app.db.models.inspection_ai_model import InspectionAIModel


def get_ai_models(
    db: Session
):

    return (
        db.query(
            InspectionAIModel
        )
        .all()
    )
