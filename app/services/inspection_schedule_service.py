from sqlalchemy.orm import Session

from app.db.models.inspection_schedule import (
    InspectionSchedule
)


def create_schedule(
    db: Session,
    data
):

    schedule = InspectionSchedule(
        **data.model_dump()
    )

    db.add(
        schedule
    )

    db.commit()

    db.refresh(
        schedule
    )

    return schedule



def get_schedules(
    db: Session
):

    return (
        db.query(
            InspectionSchedule
        )
        .all()
    )