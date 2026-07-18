from sqlalchemy.orm import Session

from app.db.models.inspection_department_rule import InspectionDepartmentRule


def get_rules(
    db: Session
):

    return (
        db.query(
            InspectionDepartmentRule
        )
        .all()
    )
