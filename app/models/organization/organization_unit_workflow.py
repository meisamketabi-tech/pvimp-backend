from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitWorkflow(Base):
    __tablename__ = "organization_unit_workflows"

    id = Column(Integer, primary_key=True, index=True)

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    workflow_id = Column(
        Integer,
        ForeignKey("organization_workflows.id"),
        nullable=False
    )

    status = Column(
        String(50),
        default="ACTIVE"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
