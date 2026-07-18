from sqlalchemy.orm import Session

from app.db.models.inspection_tag import InspectionTag


def get_tags(
    db: Session
):

    return (
        db.query(
            InspectionTag
        )
        .all()
    )
