from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISImportSchedule(Base):
    __tablename__ = "gis_import_schedules"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    cron_expression = Column(
        String(100),
    )

    template_code = Column(
        String(100),
        nullable=False,
    )

    source_path = Column(
        String(500),
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
