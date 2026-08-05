from sqlalchemy.orm import Session

from app.db.models.inspection_template import InspectionTemplate


def create_template(
    db: Session,
    data,
):
    obj = InspectionTemplate(
        **data.model_dump()
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_templates(
    db: Session,
):
    return (
        db.query(InspectionTemplate)
        .all()
    )
