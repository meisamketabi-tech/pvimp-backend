from sqlalchemy.orm import Session

from app.db.models.inspection_status_type import InspectionStatusType


def get_status_types(
    db: Session
):

    return (
        db.query(
            InspectionStatusType
        )
        .all()
    )
