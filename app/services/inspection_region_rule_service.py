from sqlalchemy.orm import Session

from app.db.models.inspection_region_rule import InspectionRegionRule


def get_region_rules(
    db: Session
):

    return (
        db.query(
            InspectionRegionRule
        )
        .all()
    )
