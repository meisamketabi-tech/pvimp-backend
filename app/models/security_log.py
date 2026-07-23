from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class SecurityLog(Base):

    __tablename__="security_logs"


    id=Column(Integer,primary_key=True)

    user_id=Column(Integer)

    action=Column(String(200))

    ip_address=Column(String(100))

    details=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
