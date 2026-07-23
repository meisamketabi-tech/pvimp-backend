from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class InspectionForm(Base):

    __tablename__="inspection_forms"


    id=Column(Integer,primary_key=True)

    title=Column(String(200))

    category=Column(String(100))

    schema_json=Column(Text)

    active=Column(Boolean,default=True)
