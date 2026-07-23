from sqlalchemy import Column,Integer,String,Date,Boolean,Text

from app.core.database import Base


class Permit(Base):

    __tablename__="permits"


    id=Column(Integer,primary_key=True)

    owner_id=Column(Integer)

    permit_type=Column(String(100))

    permit_number=Column(String(100))

    issue_date=Column(Date)

    expire_date=Column(Date)

    status=Column(String(50))

    description=Column(Text)

    active=Column(Boolean,default=True)
