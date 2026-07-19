from sqlalchemy.orm import Session

from app.db.models.inspection_status_history import InspectionStatusHistory

from app.db.models.inspection import (
    Inspection,
    InspectionType,
    Checklist,
    ChecklistItem,
    InspectionItemResult,
    InspectionStatusEnum,
)


def get_inspection(
    db: Session,
    inspection_id: int
):
    return (
        db.query(Inspection)
        .filter(
            Inspection.id == inspection_id
        )
        .first()
    )


def update_inspection_status(
    db: Session,
    inspection_id: int,
    status: InspectionStatusEnum,
    changed_by: int,
    note: str | None = None
):

    inspection = get_inspection(
        db,
        inspection_id
    )

    if not inspection:
        return None


    old_status = inspection.status


    inspection.status = status


    history = InspectionStatusHistory(
        inspection_id=inspection.id,
        old_status=old_status,
        new_status=status,
        changed_by=changed_by,
        note=note
    )


    db.add(history)

    db.commit()

    db.refresh(inspection)

    return inspection


def get_inspection_status_history(
    db: Session,
    inspection_id: int
):

    return (
        db.query(InspectionStatusHistory)
        .filter(
            InspectionStatusHistory.inspection_id == inspection_id
        )
        .order_by(
            InspectionStatusHistory.changed_at.asc()
        )
        .all()
    )
