from sqlalchemy.orm import Session

from app.db.models.inspection_deadline import InspectionDeadline


def create_deadline(
    db: Session,
    data
):

    obj = InspectionDeadline(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
