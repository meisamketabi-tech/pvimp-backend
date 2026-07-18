from sqlalchemy.orm import Session

from app.db.models.inspection_integration_log import InspectionIntegrationLog


def get_integration_logs(
    db: Session
):

    return (
        db.query(
            InspectionIntegrationLog
        )
        .all()
    )
