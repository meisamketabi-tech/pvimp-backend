from sqlalchemy.orm import Session

from app.db.models.inspection_document_type import InspectionDocumentType


def get_document_types(
    db: Session
):

    return (
        db.query(
            InspectionDocumentType
        )
        .all()
    )
