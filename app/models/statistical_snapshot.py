from sqlalchemy import Column,Integer,String,Float,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class StatisticalSnapshot(Base):

    __tablename__="statistical_snapshots"


    id=Column(Integer,primary_key=True)

    metric=Column(String(200))

    category=Column(String(100))

    value=Column(Float)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
