from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionWorkflowStep(Base):

    __tablename__ = "inspection_workflow_steps"


    id = Column(
        Integer,
        primary_key=True
    )


    workflow_id = Column(
        Integer
    )


    title = Column(
        String(200)
    )


    status = Column(
        String(50)
    )
