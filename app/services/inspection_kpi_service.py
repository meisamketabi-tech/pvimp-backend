from sqlalchemy.orm import Session

from app.db.models.inspection_kpi import InspectionKPI


def get_kpis(
    db: Session
):

    return (
        db.query(
            InspectionKPI
        )
        .all()
    )
