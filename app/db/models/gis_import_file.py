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


class GISImportFile(Base):
    __tablename__ = "gis_import_files"

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

    file_name = Column(
        String(255),
        nullable=False,
    )

    file_path = Column(
        String(500),
    )

    file_size = Column(
        Integer,
        default=0,
    )

    file_type = Column(
        String(50),
    )

    uploaded_by = Column(
        String(100),
    )

    uploaded_at = Column(
        DateTime,
        server_default=func.now(),
    )

    job = relationship(
        "GISImportJob",
        backref="files",
    )
