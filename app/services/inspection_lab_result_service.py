from sqlalchemy.orm import Session

from app.db.models.inspection_lab_result import InspectionLabResult


def create_result(
    db: Session,
    data,
):
    obj = InspectionLabResult(
        **data.model_dump()
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_results(
    db: Session,
    inspection_id: int,
):
    return (
        db.query(InspectionLabResult)
        .filter(
            InspectionLabResult.inspection_id == inspection_id
        )
        .all()
    )
