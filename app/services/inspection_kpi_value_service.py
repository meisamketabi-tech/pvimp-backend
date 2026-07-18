from sqlalchemy.orm import Session

from app.db.models.inspection_kpi_value import InspectionKPIValue


def get_kpi_values(
    db: Session
):

    return (
        db.query(
            InspectionKPIValue
        )
        .all()
    )
