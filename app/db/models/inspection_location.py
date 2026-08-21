from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from app.db.base_class import Base


class InspectionLocation(Base):

    __tablename__ = "inspection_locations"

    id = Column(
        Integer,
        primary_key=True
    )

    inspection_id = Column(
        Integer,
        ForeignKey(
            "inspections.id"
        ),
        nullable=False
    )

    address = Column(
        String(500),
        nullable=False
    )

    latitude = Column(
        String(50)
    )

    longitude = Column(
        String(50)
    )