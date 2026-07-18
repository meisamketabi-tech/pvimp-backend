from sqlalchemy.orm import Session

from app.db.models.inspection import (
    InspectionType,
    Checklist,
)


def validate_inspection_type_exists(
    db: Session,
    inspection_type_id: int
):

    return (
        db.query(InspectionType)
        .filter(
            InspectionType.id == inspection_type_id
        )
        .first()
        is not None
    )


def validate_checklist_exists(
    db: Session,
    checklist_id: int
):

    return (
        db.query(Checklist)
        .filter(
            Checklist.id == checklist_id
        )
        .first()
        is not None
    )