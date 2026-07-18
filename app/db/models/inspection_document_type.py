from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionDocumentType(Base):

    __tablename__ = "inspection_document_types"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    code = Column(
        String(50)
    )
