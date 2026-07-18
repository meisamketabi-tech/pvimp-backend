from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base


class InspectionQuestion(Base):

    __tablename__ = "inspection_questions"

    id = Column(
        Integer,
        primary_key=True
    )

    checklist_id = Column(
        Integer,
        ForeignKey("checklists.id")
    )

    text = Column(
        String(500)
    )
