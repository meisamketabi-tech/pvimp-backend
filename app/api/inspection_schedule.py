
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.db.models.inspection_schedule import InspectionSchedule



router=APIRouter(
prefix="/inspection-schedules",
tags=["Inspection Schedule"]
)



@router.post("/")
def create_schedule(
data:dict,
db:Session=Depends(get_db)
):

    obj=InspectionSchedule(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/{officer}")
def get_schedule(
officer:int,
db:Session=Depends(get_db)
):

    return db.query(
        InspectionSchedule
    ).filter(
        InspectionSchedule.officer_id==officer
    ).all()




@router.put("/{id}/complete")
def complete(
id:int,
db:Session=Depends(get_db)
):

    obj=db.query(
        InspectionSchedule
    ).filter(
        InspectionSchedule.id==id
    ).first()


    obj.completed=True


    db.commit()


    return obj

