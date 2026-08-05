from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISImportError(Base):
    __tablename__ = "gis_import_errors"

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

    field_name = Column(
        String(255),
    )

    error_code = Column(
        String(100),
    )

    error_message = Column(
        String(500),
    )

    job = relationship(
        "GISImportJob",
        backref="errors",
    )
