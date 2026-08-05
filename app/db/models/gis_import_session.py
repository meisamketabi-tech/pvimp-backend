from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.base_class import Base


class GISImportSession(Base):
    __tablename__ = "gis_import_sessions"

    id = Column(Integer, primary_key=True, index=True)

    session_key = Column(String(100), unique=True, nullable=False)

    username = Column(String(100))

    ip_address = Column(String(50))

    status = Column(String(30), default="ACTIVE")

    is_locked = Column(Boolean, default=False)

    started_at = Column(DateTime, server_default=func.now())

    finished_at = Column(DateTime)
