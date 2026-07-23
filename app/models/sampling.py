from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class Sampling(Base):

    __tablename__="sampling_records"


    id=Column(Integer,primary_key=True)

    inspection_id=Column(Integer)

    sample_type=Column(String(100))

    code=Column(String(100))

    description=Column(Text)

    status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
