from sqlalchemy.orm import Session

from app.db.models.inspection_workflow import InspectionWorkflow


def get_workflows(
    db: Session
):

    return (
        db.query(
            InspectionWorkflow
        )
        .all()
    )
