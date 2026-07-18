from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionFormField(Base):

    __tablename__ = "inspection_form_fields"


    id = Column(
        Integer,
        primary_key=True
    )


    form_id = Column(
        Integer
    )


    name = Column(
        String(200)
    )


    field_type = Column(
        String(100)
    )
