from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class MobileSync(Base):

    __tablename__="mobile_sync"


    id=Column(Integer,primary_key=True)

    user_id=Column(Integer)

    device_id=Column(String(200))

    sync_type=Column(String(100))

    status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
