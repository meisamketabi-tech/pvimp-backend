from sqlalchemy import Column,Integer,String,Boolean

from app.core.database import Base


class FormField(Base):

    __tablename__="form_fields"

    id=Column(Integer,primary_key=True)

    form_id=Column(Integer)

    label=Column(String(200))

    name=Column(String(100))

    field_type=Column(String(50))

    required=Column(Boolean,default=False)

    order_no=Column(Integer)
