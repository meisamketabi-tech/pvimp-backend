from sqlalchemy.orm import Session

from app.db.models.inspection import (
    Inspection,
    InspectionType,
    Checklist,
    ChecklistItem,
    InspectionItemResult,
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


def get_all_inspections(
    db: Session
):
    return (
        db.query(Inspection)
        .all()
    )


def delete_inspection(
    db: Session,
    inspection_id: int
):

    inspection = get_inspection(
        db,
        inspection_id
    )

    if not inspection:
        return False

    db.delete(
        inspection
    )

    db.commit()

    return True


def get_checklist(
    db: Session,
    checklist_id: int
):

    return (
        db.query(Checklist)
        .filter(
            Checklist.id == checklist_id
        )
        .first()
    )


def get_checklist_items(
    db: Session,
    checklist_id: int
):

    return (
        db.query(ChecklistItem)
        .filter(
            ChecklistItem.checklist_id == checklist_id
        )
        .all()
    )

from app.db.models.inspection import InspectionType


def create_inspection_type(
    db,
    data
):
    obj = InspectionType(
        title=data.title,
        description=data.description,
        is_active=data.is_active
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj



def get_inspection_types(
    db
):
    return (
        db.query(InspectionType)
        .all()
    )
