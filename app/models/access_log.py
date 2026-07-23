from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class AccessLog(Base):

    __tablename__="access_logs"


    id=Column(Integer,primary_key=True)

    user_id=Column(Integer)

    endpoint=Column(String(300))

    method=Column(String(20))

    ip=Column(String(100))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
