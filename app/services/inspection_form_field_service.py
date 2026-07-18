from sqlalchemy.orm import Session

from app.db.models.inspection_form_field import InspectionFormField


def get_form_fields(
    db: Session
):

    return (
        db.query(
            InspectionFormField
        )
        .all()
    )
