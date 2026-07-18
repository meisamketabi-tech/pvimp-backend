from sqlalchemy.orm import Session

from app.db.models.inspection_template import (
    InspectionTemplate
)


def create_template(
    db: Session,
    data
):

    template = InspectionTemplate(
        **data.model_dump()
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    return template



def get_templates(
    db: Session
):

    return (
        db.query(
            InspectionTemplate
        )
        .all()
    )