from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionTask(Base):

    __tablename__ = "inspection_tasks"


    id = Column(
        Integer,
        primary_key=True
    )


    inspection_id = Column(
        Integer
    )


    title = Column(
        String(300)
    )


    assigned_to = Column(
        Integer
    )


    status = Column(
        String(50)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
