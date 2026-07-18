from sqlalchemy.orm import Session

from app.db.models.inspection_source import InspectionSource


def get_sources(
    db: Session
):

    return (
        db.query(
            InspectionSource
        )
        .all()
    )
