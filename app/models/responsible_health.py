from sqlalchemy import Column,Integer,String,Date,Text,ForeignKey,DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class ResponsibleOfficer(Base):

    __tablename__="responsible_officers"

    id=Column(Integer,primary_key=True,index=True)

    full_name=Column(String(150))
    national_code=Column(String(20))
    veterinary_system_code=Column(String(50))
    license_number=Column(String(50))

    unit_name=Column(String(200))
    unit_type=Column(String(100))

    status=Column(String(50),default="فعال")

    created_at=Column(DateTime,server_default=func.now())



class NonConformity(Base):

    __tablename__="non_conformities"

    id=Column(Integer,primary_key=True)

    officer_id=Column(Integer)

    title=Column(String(200))

    level=Column(String(50))

    description=Column(Text)

    corrective_action=Column(Text)



class CorrectiveAction(Base):

    __tablename__="corrective_actions"

    id=Column(Integer,primary_key=True)

    nonconformity_id=Column(Integer)

    root_cause=Column(Text)

    action=Column(Text)

    executor=Column(String(150))



class DocumentControl(Base):

    __tablename__="document_controls"

    id=Column(Integer,primary_key=True)

    document_type=Column(String(100))

    status=Column(String(50))

    description=Column(Text)