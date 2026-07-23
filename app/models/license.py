from sqlalchemy import Column,Integer,String,Boolean,DateTime

from sqlalchemy.sql import func

from app.core.database import Base


class License(Base):

    __tablename__="licenses"


    id=Column(Integer,primary_key=True)

    owner_id=Column(Integer)

    license_type=Column(String(200))

    license_number=Column(String(100))

    issue_date=Column(DateTime)

    expire_date=Column(DateTime)

    active=Column(Boolean,default=True)

    created_at=Column(
        DateTime,
        server_default=func.now()
    )
