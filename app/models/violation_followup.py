
from sqlalchemy import Column,Integer,String,Text,Date,Boolean

from app.core.database import Base



class ViolationFollowUp(Base):

    __tablename__="violation_followups"


    id=Column(
        Integer,
        primary_key=True
    )


    violation_id=Column(
        Integer
    )


    inspector_id=Column(
        Integer
    )


    followup_date=Column(
        Date
    )


    result=Column(
        String(100)
    )


    description=Column(
        Text
    )


    resolved=Column(
        Boolean,
        default=False
    )

