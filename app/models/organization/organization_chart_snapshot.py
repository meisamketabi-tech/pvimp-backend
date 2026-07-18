from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.db.base_class import Base


class OrganizationChartSnapshot(Base):
    __tablename__ = "organization_chart_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    is_current = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
