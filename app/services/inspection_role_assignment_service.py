from sqlalchemy.orm import Session

from app.db.models.inspection_role_assignment import InspectionRoleAssignment


def get_role_assignments(
    db: Session
):

    return (
        db.query(
            InspectionRoleAssignment
        )
        .all()
    )
