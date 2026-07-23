from sqlalchemy import Column,Integer,String,Boolean

from app.core.database import Base


class UserProfile(Base):

    __tablename__="user_profiles"


    id=Column(Integer,primary_key=True)

    user_id=Column(Integer)

    first_name=Column(String(100))

    last_name=Column(String(100))

    national_code=Column(String(50))

    mobile=Column(String(50))

    active=Column(Boolean,default=True)
