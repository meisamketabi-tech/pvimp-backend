from sqlalchemy.orm import Session

from app.db.models.inspection_assignment import InspectionAssignment
from app.db.models.inspection import Inspection


def create_assignment(
    db: Session,
    data
):

    inspection = db.query(Inspection).filter(
        Inspection.id == data.inspection_id
    ).first()

    if not inspection:
        return None


    assignment = InspectionAssignment(
        inspection_id=data.inspection_id,
        inspector_id=data.inspector_id
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment



def get_assignments(
    db: Session
):

    return db.query(InspectionAssignment).all()