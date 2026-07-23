from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Sample(Base):

    __tablename__="samples"


    id=Column(Integer,primary_key=True)

    inspection_id=Column(Integer)

    sample_type=Column(String(100))

    code=Column(String(100))

    status=Column(String(50))

    result=Column(Text)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
