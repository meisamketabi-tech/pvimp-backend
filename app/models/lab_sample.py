from sqlalchemy import Column,Integer,String,Text,Date,Boolean

from app.core.database import Base


class LabSample(Base):

    __tablename__="lab_samples"


    id=Column(Integer,primary_key=True)

    inspection_id=Column(Integer)

    unit_id=Column(Integer)

    sample_code=Column(String(100))

    sample_type=Column(String(100))

    laboratory=Column(String(200))

    result=Column(String(100))

    result_detail=Column(Text)

    sampling_date=Column(Date)

    closed=Column(Boolean,default=False)
