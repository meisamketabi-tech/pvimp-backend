from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionExportTemplate(Base):

    __tablename__ = "inspection_export_templates"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    format = Column(
        String(50)
    )
