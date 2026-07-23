from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class ComplaintTracking(Base):

    __tablename__="complaint_tracking"


    id=Column(Integer,primary_key=True)

    complaint_id=Column(Integer)

    action=Column(String(200))

    performed_by=Column(Integer)

    description=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
