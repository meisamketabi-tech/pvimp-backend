from sqlalchemy import Column,Integer,String,Boolean,Text

from app.core.database import Base


class VeterinaryCenter(Base):

    __tablename__="veterinary_centers"


    id=Column(Integer,primary_key=True)

    name=Column(String(300))

    center_type=Column(String(100))

    license_number=Column(String(100))

    address=Column(Text)

    owner=Column(String(200))

    active=Column(Boolean,default=True)
