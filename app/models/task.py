from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Task(Base):

    __tablename__="tasks"


    id=Column(Integer,primary_key=True)

    title=Column(String(300))

    description=Column(Text)

    assigned_to=Column(Integer)

    priority=Column(String(50))

    status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
