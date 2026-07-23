
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.checklist import HealthChecklist

from app.models.checklist_item import HealthChecklistItem



router=APIRouter(
prefix="/checklists",
tags=["Checklists"]
)



@router.get("/")
def list_checklists(
db:Session=Depends(get_db)
):

    return db.query(
        HealthChecklist
    ).filter(
        HealthChecklist.active==True
    ).all()




@router.get("/{id}/items")
def checklist_items(
id:int,
db:Session=Depends(get_db)
):

    return db.query(
        HealthChecklistItem
    ).filter(
        HealthChecklistItem.checklist_id==id
    ).all()

