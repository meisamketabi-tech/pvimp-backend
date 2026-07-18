from sqlalchemy.orm import Session

from app.db.models.inspection_approval import InspectionApproval


def get_approvals(
    db: Session
):

    return (
        db.query(
            InspectionApproval
        )
        .all()
    )
