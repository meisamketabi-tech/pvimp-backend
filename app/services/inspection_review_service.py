from sqlalchemy.orm import Session

from app.db.models.inspection_review import InspectionReview


def create_review(
    db: Session,
    data
):

    obj = InspectionReview(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
