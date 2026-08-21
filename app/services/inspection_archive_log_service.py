from sqlalchemy.orm import Session

from app.db.models.inspection_archive_log import InspectionArchiveLog


def get_archive_logs(
    db: Session
):

    return (
        db.query(
            InspectionArchiveLog
        )
        .all()
    )
