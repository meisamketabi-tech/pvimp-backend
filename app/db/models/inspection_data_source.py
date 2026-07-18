from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionDataSource(Base):

    __tablename__ = "inspection_data_sources"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    connection_type = Column(
        String(100)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
