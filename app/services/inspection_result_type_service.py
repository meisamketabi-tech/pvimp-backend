from sqlalchemy.orm import Session

from app.db.models.inspection_result_type import InspectionResultType


def get_result_types(
    db: Session
):

    return (
        db.query(
            InspectionResultType
        )
        .all()
    )
