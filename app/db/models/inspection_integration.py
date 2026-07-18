from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionIntegration(Base):

    __tablename__ = "inspection_integrations"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    endpoint = Column(
        String(500)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
