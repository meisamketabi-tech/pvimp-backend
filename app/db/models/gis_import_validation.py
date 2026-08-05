from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GISImportValidation(Base):
    __tablename__ = "gis_import_validation"

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

    validation_type = Column(
        String(100),
    )

    message = Column(
        String(500),
    )

    status = Column(
        String(30),
        default="FAILED",
    )

    job = relationship(
        "GISImportJob",
        backref="validations",
    )
