from sqlalchemy.orm import Session

from app.db.models.inspection_sync_log import InspectionSyncLog


def get_sync_logs(
    db: Session
):

    return (
        db.query(
            InspectionSyncLog
        )
        .all()
    )
