from sqlalchemy.orm import Session

from app.db.models.inspection_import import InspectionImport


def get_imports(
    db: Session
):

    return (
        db.query(
            InspectionImport
        )
        .all()
    )
