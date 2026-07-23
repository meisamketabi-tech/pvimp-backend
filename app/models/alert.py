from sqlalchemy import Column,Integer,String,Text,Boolean,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Alert(Base):

    __tablename__="alerts"


    id=Column(Integer,primary_key=True)

    alert_type=Column(String(100))

    priority=Column(String(50))

    title=Column(String(300))

    message=Column(Text)

    resolved=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
