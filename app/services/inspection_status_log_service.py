from sqlalchemy.orm import Session

from app.db.models.inspection_status_log import InspectionStatusLog


def get_status_logs(
    db: Session,
    inspection_id: int
):

    return (
        db.query(
            InspectionStatusLog
        )
        .filter(
            InspectionStatusLog.inspection_id == inspection_id
        )
        .all()
    )
