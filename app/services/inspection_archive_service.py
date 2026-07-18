from sqlalchemy.orm import Session

from app.db.models.inspection_archive import InspectionArchive


def create_archive(
    db: Session,
    data
):

    obj = InspectionArchive(
        **data.model_dump()
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj
