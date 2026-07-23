from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class ReportTemplate(Base):

    __tablename__="report_templates"


    id=Column(Integer,primary_key=True)

    title=Column(String(200))

    code=Column(String(100))

    structure=Column(Text)

    active=Column(Boolean,default=True)
