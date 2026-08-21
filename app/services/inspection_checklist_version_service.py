from sqlalchemy.orm import Session

from app.db.models.inspection_checklist_version import InspectionChecklistVersion


def get_checklist_versions(
    db: Session
):

    return (
        db.query(
            InspectionChecklistVersion
        )
        .all()
    )
