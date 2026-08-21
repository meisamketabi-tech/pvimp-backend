from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISImportQueue(Base):
    __tablename__ = "gis_import_queue"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_type = Column(
        String(100),
        nullable=False,
    )

    payload = Column(
        String,
    )

    status = Column(
        String(50),
        default="WAITING",
    )

    priority = Column(
        Integer,
        default=1,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    started_at = Column(
        DateTime,
    )

    finished_at = Column(
        DateTime,
    )
