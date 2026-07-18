from sqlalchemy.orm import Session

from app.db.models.inspection_assignment_history import InspectionAssignmentHistory


def get_assignment_history(
    db: Session
):

    return (
        db.query(
            InspectionAssignmentHistory
        )
        .all()
    )
