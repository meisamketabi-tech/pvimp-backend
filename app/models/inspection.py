from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Inspection(Base):

    __tablename__="inspections"


    id=Column(Integer,primary_key=True)

    inspector_id=Column(Integer)

    entity_type=Column(String(100))

    entity_id=Column(Integer)

    inspection_type=Column(String(100))

    findings=Column(Text)

    status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
