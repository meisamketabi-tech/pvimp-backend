from sqlalchemy.orm import Session

from app.db.models.inspection_source_type import InspectionSourceType


def get_source_types(
    db: Session
):

    return (
        db.query(
            InspectionSourceType
        )
        .all()
    )
