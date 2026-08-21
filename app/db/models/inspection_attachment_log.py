from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionAttachmentLog(Base):

    __tablename__ = "inspection_attachment_logs"


    id = Column(
        Integer,
        primary_key=True
    )


    attachment_id = Column(
        Integer
    )


    action = Column(
        String(100)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
