from sqlalchemy.orm import Session

from app.db.models.inspection_audit import InspectionAudit


def get_audits(
    db: Session
):

    return (
        db.query(
            InspectionAudit
        )
        .all()
    )
