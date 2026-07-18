from sqlalchemy.orm import Session

from app.db.models.inspection_execution import InspectionExecution


def get_executions(
    db: Session
):

    return (
        db.query(
            InspectionExecution
        )
        .all()
    )
