from sqlalchemy import Column,Integer,String,Boolean,Text

from app.core.database import Base


class FormBuilder(Base):

    __tablename__="form_builders"

    id=Column(Integer,primary_key=True)

    title=Column(String(200))

    code=Column(String(100),unique=True)

    description=Column(Text)

    version=Column(Integer,default=1)

    active=Column(Boolean,default=True)
