from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    action = Column(String(200))

    entity = Column(String(100))

    entity_id = Column(Integer)

    details = Column(Text)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )