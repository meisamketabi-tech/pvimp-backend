from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class SyncLog(Base):

    __tablename__="sync_logs"


    id=Column(Integer,primary_key=True)

    system_name=Column(String(200))

    operation=Column(String(100))

    status=Column(String(50))

    details=Column(String(500))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
