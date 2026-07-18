from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationPosition(Base):
    __tablename__ = "organization_positions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    position_type = Column(
        String(50),
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=True
    )

    is_managerial = Column(
        Boolean,
        default=False,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    roles = relationship(
        "OrganizationRole",
        back_populates="position"
    )
