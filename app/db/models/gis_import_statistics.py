from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISImportStatistics(Base):
    __tablename__ = "gis_import_statistics"

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

    total_rows = Column(
        Integer,
        default=0,
    )

    imported_rows = Column(
        Integer,
        default=0,
    )

    duplicate_rows = Column(
        Integer,
        default=0,
    )

    invalid_rows = Column(
        Integer,
        default=0,
    )

    skipped_rows = Column(
        Integer,
        default=0,
    )

    job = relationship(
        "GISImportJob",
        backref="statistics",
    )
