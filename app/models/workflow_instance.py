from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class WorkflowInstance(Base):

    __tablename__="workflow_instances"


    id=Column(Integer,primary_key=True)

    workflow_code=Column(String(100))

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    current_state=Column(String(100))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
