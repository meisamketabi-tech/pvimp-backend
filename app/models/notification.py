from sqlalchemy import Column,Integer,String,Text,Boolean,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Notification(Base):

    __tablename__="notifications"


    id=Column(Integer,primary_key=True)

    user_id=Column(Integer)

    title=Column(String(300))

    message=Column(Text)

    notification_type=Column(String(100))

    read=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
