from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

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

    name = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    is_management = Column(
        Boolean,
        default=False,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    assignments = relationship(
        "UserAssignment",
        back_populates="position"
    )
