from sqlalchemy.orm import Session

from app.db.models.inspection_zone import InspectionZone


def get_zones(
    db: Session
):

    return (
        db.query(
            InspectionZone
        )
        .all()
    )
