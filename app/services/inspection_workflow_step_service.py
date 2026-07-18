from sqlalchemy.orm import Session

from app.db.models.inspection_workflow_step import InspectionWorkflowStep


def get_workflow_steps(
    db: Session
):

    return (
        db.query(
            InspectionWorkflowStep
        )
        .all()
    )
