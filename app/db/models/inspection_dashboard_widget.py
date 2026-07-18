from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class InspectionDashboardWidget(Base):

    __tablename__ = "inspection_dashboard_widgets"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String(200)
    )


    widget_type = Column(
        String(100)
    )
