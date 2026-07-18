from sqlalchemy.orm import Session

from app.db.models.inspection_task import InspectionTask


def get_tasks(
    db: Session
):

    return (
        db.query(
            InspectionTask
        )
        .all()
    )
