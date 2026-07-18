from sqlalchemy.orm import Session

from app.db.models.inspection_sample import InspectionSample


def create_sample(
    db: Session,
    data
):

    obj = InspectionSample(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
