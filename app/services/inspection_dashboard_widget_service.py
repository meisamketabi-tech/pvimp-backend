from sqlalchemy.orm import Session

from app.db.models.inspection_dashboard_widget import InspectionDashboardWidget


def get_widgets(
    db: Session
):

    return (
        db.query(
            InspectionDashboardWidget
        )
        .all()
    )
