from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.db.base_class import Base


class OrganizationDocument(Base):
    __tablename__ = "organization_documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(300),
        nullable=False
    )

    document_type = Column(
        String(100),
        nullable=False
    )

    file_path = Column(
        String(500),
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
