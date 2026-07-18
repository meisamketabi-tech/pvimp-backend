from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionChecklistVersion(Base):

    __tablename__ = "inspection_checklist_versions"


    id = Column(
        Integer,
        primary_key=True
    )


    checklist_id = Column(
        Integer
    )


    version = Column(
        String(50)
    )
