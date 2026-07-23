from sqlalchemy import Column,Integer,String,Text,Boolean

from app.core.database import Base


class WorkflowDefinition(Base):

    __tablename__="workflow_definitions"


    id=Column(Integer,primary_key=True)

    name=Column(String(200))

    entity_type=Column(String(100))

    states=Column(Text)

    transitions=Column(Text)

    active=Column(Boolean,default=True)
