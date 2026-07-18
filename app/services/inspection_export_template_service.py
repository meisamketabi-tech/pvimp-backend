from sqlalchemy.orm import Session

from app.db.models.inspection_export_template import InspectionExportTemplate


def get_export_templates(
    db: Session
):

    return (
        db.query(
            InspectionExportTemplate
        )
        .all()
    )
