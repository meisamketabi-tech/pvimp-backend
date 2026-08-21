from sqlalchemy.orm import Session

from app.db.models.inspection_communication import InspectionCommunication


def create_communication(
    db: Session,
    data
):

    obj = InspectionCommunication(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
