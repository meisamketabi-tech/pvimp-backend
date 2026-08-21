from sqlalchemy.orm import Session

from app.db.models.inspection_attachment_type import InspectionAttachmentType


def get_attachment_types(
    db: Session
):

    return (
        db.query(
            InspectionAttachmentType
        )
        .all()
    )
