from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class OrganizationUnitDocument(Base):
    __tablename__ = "organization_unit_documents"

    id = Column(Integer, primary_key=True, index=True)

    organization_unit_id = Column(
        Integer,
        ForeignKey("organization_units.id"),
        nullable=False
    )

    document_id = Column(
        Integer,
        ForeignKey("organization_documents.id"),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
