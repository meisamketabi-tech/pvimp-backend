from sqlalchemy.orm import Session

from app.db.models.inspection_score import (
    InspectionScore
)


def calculate_score(
    db: Session,
    inspection_id: int
):

    score = InspectionScore(
        inspection_id=inspection_id,
        total_score=0,
        max_score=0
    )

    db.add(score)
    db.commit()
    db.refresh(score)

    return score