from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.db.base_class import Base


class OrganizationLevel(Base):
    __tablename__ = "organization_levels"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False,
        unique=True
    )

    order = Column(
        Integer,
        nullable=False
    )

    description = Column(
        String(500),
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
