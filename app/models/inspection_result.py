
from sqlalchemy import Column,Integer,String,Text,Date

from app.core.database import Base



class InspectionResult(Base):

    __tablename__="inspection_results"


    id=Column(
        Integer,
        primary_key=True
    )


    inspection_id=Column(
        Integer
    )


    checklist_id=Column(
        Integer
    )


    inspector_id=Column(
        Integer
    )


    score=Column(
        Integer
    )


    result=Column(
        String(100)
    )


    findings=Column(
        Text
    )


    inspection_date=Column(
        Date
    )

