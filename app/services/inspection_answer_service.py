from sqlalchemy.orm import Session

from app.db.models.inspection_answer import InspectionAnswer


def create_answer(
    db: Session,
    data
):

    obj = InspectionAnswer(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
