from sqlalchemy.orm import Session

from app.db.models.inspection_template_version import InspectionTemplateVersion


def get_template_versions(
    db: Session
):

    return (
        db.query(
            InspectionTemplateVersion
        )
        .all()
    )
