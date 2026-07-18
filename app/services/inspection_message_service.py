from sqlalchemy.orm import Session

from app.db.models.inspection_message import InspectionMessage


def get_messages(
    db: Session
):

    return (
        db.query(
            InspectionMessage
        )
        .all()
    )
