from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.inspection import (
    Inspection,
    InspectionType,
    Checklist,
    ChecklistItem,
    InspectionItemResult,
)

from app.schemas.inspection import (
    InspectionCreate,
    InspectionUpdate,
    InspectionTypeCreate,
    InspectionTypeUpdate,
    ChecklistCreate,
)


# -------------------------
# Inspection Type Services
# -------------------------

def create_inspection_type(
    db: Session,
    data: InspectionTypeCreate
):
    inspection_type = InspectionType(
        **data.model_dump()
    )

    db.add(inspection_type)
    db.commit()
    db.refresh(inspection_type)

    return inspection_type


def get_inspection_types(
    db: Session
):
    return (
        db.query(InspectionType)
        .all()
    )


def get_inspection_type(
    db: Session,
    inspection_type_id: int
):
    return (
        db.query(InspectionType)
        .filter(
            InspectionType.id == inspection_type_id
        )
        .first()
    )


def update_inspection_type(
    db: Session,
    inspection_type_id: int,
    data: InspectionTypeUpdate
):
    inspection_type = get_inspection_type(
        db,
        inspection_type_id
    )

    if not inspection_type:
        return None

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():
        setattr(
            inspection_type,
            key,
            value
        )

    db.commit()
    db.refresh(inspection_type)

    return inspection_type


# -------------------------
# Checklist Services
# -------------------------

def create_checklist(
    db: Session,
    data: ChecklistCreate
):

    checklist = Checklist(
        inspection_type_id=data.inspection_type_id,
        title=data.title,
        description=data.description,
        is_active=data.is_active
    )

    db.add(checklist)
    db.flush()


    for item in data.items:

        checklist_item = ChecklistItem(
            checklist_id=checklist.id,
            **item.model_dump()
        )

        db.add(checklist_item)


    db.commit()
    db.refresh(checklist)

    return checklist


def get_checklists(
    db: Session
):

    return (
        db.query(Checklist)
        .all()
    )


# -------------------------
# Inspection Services
# -------------------------

def create_inspection(
    db: Session,
    data: InspectionCreate
):

    inspection = Inspection(
        inspection_number=
        f"INSP-{datetime_now_string()}",
        inspection_type_id=data.inspection_type_id,
        organization_unit_id=data.organization_unit_id,
        inspector_id=data.inspector_id,
        inspection_date=data.inspection_date,
        notes=data.notes
    )

    db.add(inspection)
    db.flush()


    for item in data.items_result:

        result = InspectionItemResult(
            inspection_id=inspection.id,
            **item.model_dump()
        )

        db.add(result)


    db.commit()
    db.refresh(inspection)

    return inspection


def get_inspections(
    db: Session
):

    return (
        db.query(Inspection)
        .all()
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


def update_inspection(
    db: Session,
    inspection_id: int,
    data: InspectionUpdate
):

    inspection = get_inspection(
        db,
        inspection_id
    )

    if not inspection:
        return None


    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            inspection,
            key,
            value
        )


    db.commit()
    db.refresh(inspection)

    return inspection


# -------------------------
# Helpers
# -------------------------

def datetime_now_string():

    from datetime import datetime

    return datetime.utcnow().strftime(
        "%Y%m%d%H%M%S"
    )