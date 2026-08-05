from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISImportLog(Base):
    __tablename__ = "gis_import_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_id = Column(
        Integer,
        ForeignKey("gis_import_jobs.id"),
        nullable=False,
        index=True,
    )

    level = Column(
        String(30),
        default="INFO",
    )

    message = Column(
        String(500),
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    job = relationship(
        "GISImportJob",
        backref="logs",
    )
