from sqlalchemy.orm import Session

from app.db.models.inspection_document import InspectionDocument


def create_document(
    db: Session,
    data
):

    obj = InspectionDocument(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
