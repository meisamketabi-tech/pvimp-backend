from sqlalchemy.orm import Session

from app.db.models.inspection_form import InspectionForm


def get_forms(
    db: Session
):

    return (
        db.query(
            InspectionForm
        )
        .all()
    )
