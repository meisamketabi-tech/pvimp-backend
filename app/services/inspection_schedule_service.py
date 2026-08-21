from sqlalchemy.orm import Session

from app.db.models.inspection_schedule import InspectionSchedule


def create_schedule(
    db: Session,
    data,
):
    obj = InspectionSchedule(
        **data.model_dump()
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_schedules(
    db: Session,
):
    return (
        db.query(InspectionSchedule)
        .all()
    )
