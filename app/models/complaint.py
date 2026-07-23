from sqlalchemy import Column,Integer,String,Text,DateTime,Boolean

from sqlalchemy.sql import func

from app.core.database import Base


class Complaint(Base):

    __tablename__="complaints"


    id=Column(Integer,primary_key=True)

    citizen_name=Column(String(200))

    contact=Column(String(100))

    subject=Column(String(300))

    description=Column(Text)

    status=Column(String(50))

    anonymous=Column(Boolean,default=False)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
