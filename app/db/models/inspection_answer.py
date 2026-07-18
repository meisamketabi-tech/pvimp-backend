from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.db.base_class import Base


class InspectionAnswer(Base):

    __tablename__ = "inspection_answers"

    id = Column(
        Integer,
        primary_key=True
    )

    question_id = Column(
        Integer,
        ForeignKey("inspection_questions.id")
    )

    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id")
    )

    answer = Column(
        String(500)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
