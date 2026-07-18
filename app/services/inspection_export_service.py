from sqlalchemy.orm import Session

from app.db.models.inspection_export import InspectionExport


def create_export(
    db: Session,
    data
):

    obj = InspectionExport(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
