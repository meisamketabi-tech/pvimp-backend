from sqlalchemy.orm import Session

from app.db.models.inspection_report_template import InspectionReportTemplate


def get_report_templates(
    db: Session
):

    return (
        db.query(
            InspectionReportTemplate
        )
        .all()
    )
