from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISImportTemplate(Base):
    __tablename__ = "gis_import_templates"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    code = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        String(500),
    )

    entity_name = Column(
        String(100),
        nullable=False,
    )

    version = Column(
        String(50),
        default="1.0",
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )
