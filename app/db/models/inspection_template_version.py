from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionTemplateVersion(Base):

    __tablename__ = "inspection_template_versions"


    id = Column(
        Integer,
        primary_key=True
    )


    template_id = Column(
        Integer
    )


    version = Column(
        String(50)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
