from sqlalchemy.orm import Session

from app.db.models.inspection_risk_assessment import InspectionRiskAssessment


def create_assessment(
    db: Session,
    data
):

    obj = InspectionRiskAssessment(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
