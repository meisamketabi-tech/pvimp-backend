from sqlalchemy import Column,Integer,String,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class UnitActivity(Base):

    __tablename__="unit_activities"


    id=Column(Integer,primary_key=True)

    unit_id=Column(Integer)

    activity_type=Column(String(100))

    description=Column(String(500))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
