from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class UserActivity(Base):

    __tablename__="user_activities"


    id=Column(Integer,primary_key=True)

    user_id=Column(Integer)

    activity=Column(String(300))

    ip_address=Column(String(100))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
