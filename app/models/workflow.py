
from sqlalchemy import Column,Integer,String,Text,DateTime
from sqlalchemy.sql import func

from app.core.database import Base



class WorkflowTask(Base):

    __tablename__="workflow_tasks"


    id=Column(Integer,primary_key=True)


    entity_type=Column(String(100))


    entity_id=Column(Integer)


    current_status=Column(
        String(50),
        default="ثبت اولیه"
    )


    assigned_to=Column(Integer)


    comment=Column(Text)


    created_at=Column(
        DateTime,
        server_default=func.now()
    )


    updated_at=Column(
        DateTime,
        onupdate=func.now()
    )

