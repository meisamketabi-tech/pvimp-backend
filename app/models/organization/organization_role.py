from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class OrganizationRole(Base):
    __tablename__ = "organization_roles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_position_id = Column(
        Integer,
        ForeignKey("organization_positions.id"),
        nullable=False
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

    level = Column(
        Integer,
        nullable=False,
        default=1
    )

    description = Column(
        String(1000),
        nullable=True
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


    position = relationship(
        "OrganizationPosition",
        backref="roles"
    )
