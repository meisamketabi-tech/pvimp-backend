from sqlalchemy.orm import Session

from app.db.models.inspection_review import InspectionReview


def create_review(
    db: Session,
    data,
):
    obj = InspectionReview(
        **data.model_dump()
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_reviews(
    db: Session,
    inspection_id: int,
):
    return (
        db.query(InspectionReview)
        .filter(
            InspectionReview.inspection_id == inspection_id
        )
        .all()
    )
