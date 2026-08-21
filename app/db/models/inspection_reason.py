from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionReason(Base):

    __tablename__ = "inspection_reasons"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String(300)
    )

    category = Column(
        String(100)
    )
