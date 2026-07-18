from sqlalchemy.orm import Session

from app.db.models.inspection_department import InspectionDepartment


def get_departments(
    db: Session
):

    return (
        db.query(
            InspectionDepartment
        )
        .all()
    )
