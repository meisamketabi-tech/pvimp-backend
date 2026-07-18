from sqlalchemy.orm import Session

from app.db.models.inspection_permission_rule import InspectionPermissionRule


def get_permission_rules(
    db: Session
):

    return (
        db.query(
            InspectionPermissionRule
        )
        .all()
    )
