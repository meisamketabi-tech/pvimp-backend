from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionSeverity(Base):

    __tablename__ = "inspection_severities"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String(200)
    )

    score = Column(
        Integer,
        default=1
    )
