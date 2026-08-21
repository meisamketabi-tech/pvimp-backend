from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionForm(Base):

    __tablename__ = "inspection_forms"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    version = Column(
        String(50)
    )
