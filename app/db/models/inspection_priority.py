from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.db.base_class import Base


class InspectionPriority(Base):

    __tablename__ = "inspection_priorities"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(100),
        nullable=False
    )


    level = Column(
        Integer,
        default=1
    )