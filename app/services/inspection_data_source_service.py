from sqlalchemy.orm import Session

from app.db.models.inspection_data_source import InspectionDataSource


def get_data_sources(
    db: Session
):

    return (
        db.query(
            InspectionDataSource
        )
        .all()
    )
