from sqlalchemy.orm import Session

from app.db.models.inspection_checklist_category import InspectionChecklistCategory


def get_checklist_categories(
    db: Session
):

    return (
        db.query(
            InspectionChecklistCategory
        )
        .all()
    )
