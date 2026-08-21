from sqlalchemy.orm import Session

from app.db.models.inspection_attachment import (
    InspectionAttachment
)


def create_attachment(
    db: Session,
    data
):

    attachment = InspectionAttachment(
        **data.model_dump()
    )


    db.add(
        attachment
    )

    db.commit()

    db.refresh(
        attachment
    )

    return attachment



def get_attachments(
    db: Session,
    inspection_id: int
):

    return (
        db.query(
            InspectionAttachment
        )
        .filter(
            InspectionAttachment.inspection_id
            ==
            inspection_id
        )
        .all()
    )