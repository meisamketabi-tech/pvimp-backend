from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.db.base_class import Base


class OrganizationRegion(Base):
    __tablename__ = "organization_regions"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(
        String(50),
        unique=True,
        nullable=False
    )

    name = Column(
        String(200),
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
