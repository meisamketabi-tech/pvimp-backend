from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class WorkflowHistory(Base):

    __tablename__="workflow_history"


    id=Column(Integer,primary_key=True)

    instance_id=Column(Integer)

    from_state=Column(String(100))

    to_state=Column(String(100))

    action=Column(String(200))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
