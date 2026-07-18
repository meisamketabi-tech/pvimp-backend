from sqlalchemy.orm import Session

from app.db.models.inspection_organization_role import InspectionOrganizationRole


def get_organization_roles(
    db: Session
):

    return (
        db.query(
            InspectionOrganizationRole
        )
        .all()
    )
