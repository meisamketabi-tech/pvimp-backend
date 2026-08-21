from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionAIModel(Base):

    __tablename__ = "inspection_ai_models"


    id = Column(
        Integer,
        primary_key=True
    )


    name = Column(
        String(200)
    )


    version = Column(
        String(50)
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
