
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.export_report import ExportReport



router=APIRouter(
prefix="/reports",
tags=["Reports"]
)



@router.post("/create")
def create_report(
data:dict,
db:Session=Depends(get_db)
):

    obj=ExportReport(
        **data
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj




@router.get("/")
def list_reports(
db:Session=Depends(get_db)
):

    return db.query(
        ExportReport
    ).order_by(
        ExportReport.id.desc()
    ).all()

