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


class GISImportHistory(Base):
    __tablename__ = "gis_import_history"

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

    action = Column(
        String(100),
        nullable=False,
    )

    username = Column(
        String(100),
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    job = relationship(
        "GISImportJob",
        backref="history",
    )
