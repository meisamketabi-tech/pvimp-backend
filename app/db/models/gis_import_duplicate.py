from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISImportDuplicate(Base):
    __tablename__ = "gis_import_duplicate"

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

    row_number = Column(
        Integer,
    )

    duplicate_key = Column(
        String(255),
    )

    existing_data = Column(
        JSON,
    )

    job = relationship(
        "GISImportJob",
        backref="duplicates",
    )
