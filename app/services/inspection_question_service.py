from sqlalchemy.orm import Session

from app.db.models.inspection_question import InspectionQuestion


def get_questions(
    db: Session
):

    return (
        db.query(
            InspectionQuestion
        )
        .all()
    )
