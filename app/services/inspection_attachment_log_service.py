from sqlalchemy.orm import Session

from app.db.models.inspection_attachment_log import InspectionAttachmentLog


def get_attachment_logs(
    db: Session
):

    return (
        db.query(
            InspectionAttachmentLog
        )
        .all()
    )
