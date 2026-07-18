from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionStatusType(Base):

    __tablename__ = "inspection_status_types"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(100)
    )


    code = Column(
        String(50)
    )
