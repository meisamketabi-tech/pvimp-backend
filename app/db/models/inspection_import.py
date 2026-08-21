from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionImport(Base):

    __tablename__ = "inspection_imports"


    id = Column(
        Integer,
        primary_key=True
    )


    file_name = Column(
        String(300)
    )


    status = Column(
        String(100)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
