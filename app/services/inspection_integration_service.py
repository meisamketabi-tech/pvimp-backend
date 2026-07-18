from sqlalchemy.orm import Session

from app.db.models.inspection_integration import InspectionIntegration


def get_integrations(
    db: Session
):

    return (
        db.query(
            InspectionIntegration
        )
        .all()
    )
