from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class InspectionAttachment(Base):

    __tablename__ = "inspection_attachments"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    inspection_id = Column(
        Integer,
        ForeignKey(
            "inspections.id"
        ),
        nullable=False
    )


    file_name = Column(
        String(255),
        nullable=False
    )


    file_path = Column(
        String(500),
        nullable=False
    )


    description = Column(
        Text,
        nullable=True
    )


    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    inspection = relationship(
        "Inspection"
    )