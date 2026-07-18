from sqlalchemy.orm import Session

from app.db.models.inspection_area import InspectionArea


def get_areas(
    db: Session
):

    return (
        db.query(
            InspectionArea
        )
        .all()
    )
