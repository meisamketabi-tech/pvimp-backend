from sqlalchemy.orm import Session

from app.db.models.inspection_category import InspectionCategory


def get_categories(
    db: Session
):

    return (
        db.query(
            InspectionCategory
        )
        .all()
    )
