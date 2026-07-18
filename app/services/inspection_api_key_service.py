from sqlalchemy.orm import Session

from app.db.models.inspection_api_key import InspectionApiKey


def get_api_keys(
    db: Session
):

    return (
        db.query(
            InspectionApiKey
        )
        .all()
    )
