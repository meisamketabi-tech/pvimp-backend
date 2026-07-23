from sqlalchemy import Column,Integer,String,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class WorkAssignment(Base):

    __tablename__="work_assignments"


    id=Column(Integer,primary_key=True)

    task_id=Column(Integer)

    assigned_to=Column(Integer)

    assigned_by=Column(Integer)

    status=Column(String(50))

    accepted=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
