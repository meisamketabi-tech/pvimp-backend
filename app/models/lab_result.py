from sqlalchemy import Column,Integer,String,Text,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class LabResult(Base):

    __tablename__="lab_results"


    id=Column(Integer,primary_key=True)

    sample_id=Column(Integer)

    laboratory=Column(String(200))

    test_name=Column(String(200))

    result_value=Column(Text)

    result_status=Column(String(50))

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
