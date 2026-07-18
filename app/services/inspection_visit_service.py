from sqlalchemy.orm import Session

from app.db.models.inspection_visit import InspectionVisit


def get_visits(
    db: Session
):

    return (
        db.query(
            InspectionVisit
        )
        .all()
    )
