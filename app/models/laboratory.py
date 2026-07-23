from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class LaboratoryRequest(Base):

    __tablename__="laboratory_requests"


    id=Column(Integer,primary_key=True)

    sample_id=Column(Integer)

    lab_name=Column(String(200))

    test_type=Column(String(200))

    result=Column(Text)

    status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
