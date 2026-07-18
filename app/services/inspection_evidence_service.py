from sqlalchemy.orm import Session

from app.db.models.inspection_evidence import (
    InspectionEvidence
)


def create_evidence(
    db: Session,
    data
):

    evidence = InspectionEvidence(
        **data.model_dump()
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence