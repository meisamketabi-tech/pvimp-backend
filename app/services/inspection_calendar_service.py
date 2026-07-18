from sqlalchemy.orm import Session

from app.db.models.inspection_calendar import InspectionCalendar


def get_calendar(
    db: Session
):

    return (
        db.query(
            InspectionCalendar
        )
        .all()
    )
