from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class WorkflowTemplate(Base):

    __tablename__="workflow_templates"


    id=Column(Integer,primary_key=True)

    name=Column(String(300))

    code=Column(String(100))

    description=Column(Text)

    definition=Column(Text)

    active=Column(Boolean,default=True)
