from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)

from app.db.base_class import Base


class InspectionTemplate(Base):

    __tablename__ = "inspection_templates"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200),
        nullable=False
    )


    description = Column(
        Text
    )