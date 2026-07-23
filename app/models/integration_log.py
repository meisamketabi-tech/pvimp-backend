from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class IntegrationLog(Base):

    __tablename__="integration_logs"


    id=Column(Integer,primary_key=True)

    system_name=Column(String(100))

    operation=Column(String(200))

    status=Column(String(50))

    response=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
