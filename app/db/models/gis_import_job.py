from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISImportJob(Base):
    __tablename__ = "gis_import_jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    template_id = Column(
        Integer,
        ForeignKey("gis_import_templates.id"),
        nullable=False,
        index=True,
    )

    session_id = Column(
        Integer,
        ForeignKey("gis_import_sessions.id"),
        nullable=True,
        index=True,
    )

    job_code = Column(
        String(100),
        unique=True,
        index=True,
    )

    status = Column(
        String(50),
        default="CREATED",
    )

    total_rows = Column(
        Integer,
        default=0,
    )

    processed_rows = Column(
        Integer,
        default=0,
    )

    success_rows = Column(
        Integer,
        default=0,
    )

    failed_rows = Column(
        Integer,
        default=0,
    )

    is_completed = Column(
        Boolean,
        default=False,
    )

    started_at = Column(
        DateTime,
    )

    finished_at = Column(
        DateTime,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    template = relationship(
        "GISImportTemplate",
        backref="jobs",
    )

    session = relationship(
        "GISImportSession",
        backref="jobs",
    )
