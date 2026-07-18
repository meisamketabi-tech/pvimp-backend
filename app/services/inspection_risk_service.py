from sqlalchemy.orm import Session

from app.db.models.inspection_risk import InspectionRisk


def get_risks(
    db: Session
):

    return (
        db.query(InspectionRisk)
        .all()
    )
