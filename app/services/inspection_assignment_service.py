from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models.inspection_assignment import InspectionAssignment
from app.db.models.inspection import Inspection


def create_assignment(
    db: Session,
    data,
    assigned_by: int | None = None,
):

    inspection = (
        db.query(Inspection)
        .filter(
            Inspection.id == data.inspection_id
        )
        .first()
    )

    if not inspection:
        return None


    active_assignment = (
        db.query(InspectionAssignment)
        .filter(
            InspectionAssignment.inspection_id == data.inspection_id,
            InspectionAssignment.is_active == True
        )
        .first()
    )

    if active_assignment:
        active_assignment.is_active = False
        active_assignment.unassigned_at = datetime.utcnow()


    assignment = InspectionAssignment(
        inspection_id=data.inspection_id,
        inspector_id=data.inspector_id,
        assigned_by=assigned_by,
        note=getattr(data, "note", None),
        is_active=True,
    )


    db.add(assignment)

    db.commit()

    db.refresh(assignment)

    return assignment



def get_assignments(
    db: Session
):

    return (
        db.query(InspectionAssignment)
        .order_by(
            InspectionAssignment.id.desc()
        )
        .all()
    )



def get_inspection_assignments(
    db: Session,
    inspection_id: int
):

    return (
        db.query(InspectionAssignment)
        .filter(
            InspectionAssignment.inspection_id == inspection_id
        )
        .order_by(
            InspectionAssignment.id.desc()
        )
        .all()
    )



def unassign_inspection(
    db: Session,
    assignment_id: int
):

    assignment = (
        db.query(InspectionAssignment)
        .filter(
            InspectionAssignment.id == assignment_id
        )
        .first()
    )

    if not assignment:
        return None


    assignment.is_active = False
    assignment.unassigned_at = datetime.utcnow()


    db.commit()

    db.refresh(assignment)

    return assignment