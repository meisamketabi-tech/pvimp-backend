from sqlalchemy.orm import Session

from app.db.models.inspection_status_history import InspectionStatusHistory


def get_history(
    db: Session,
    inspection_id: int
):

    return (
        db.query(
            InspectionStatusHistory
        )
        .filter(
            InspectionStatusHistory.inspection_id == inspection_id
        )
        .all()
    )
