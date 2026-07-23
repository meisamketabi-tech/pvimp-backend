from sqlalchemy import Column,Integer,Float,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class LocationHistory(Base):

    __tablename__="location_history"


    id=Column(Integer,primary_key=True)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    latitude=Column(Float)

    longitude=Column(Float)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
