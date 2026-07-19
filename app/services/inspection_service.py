from sqlalchemy.orm import Session

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
    status: InspectionStatusEnum
):

    inspection = get_inspection(
        db,
        inspection_id
    )

    if not inspection:
        return None

    inspection.status = status

    db.commit()
    db.refresh(inspection)

    return inspection