
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.reminder import HealthReminder



router=APIRouter(
prefix="/reminders",
tags=["Reminders"]
)



@router.post("/")
def create(
data:dict,
db:Session=Depends(get_db)
):

    obj=HealthReminder(
        **data
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj




@router.get("/")
def list_all(
db:Session=Depends(get_db)
):

    return db.query(
        HealthReminder
    ).filter(
        HealthReminder.completed==False
    ).all()




@router.put("/{id}/complete")
def complete(
id:int,
db:Session=Depends(get_db)
):

    obj=db.query(
        HealthReminder
    ).filter(
        HealthReminder.id==id
    ).first()


    obj.completed=True

    db.commit()

    return obj

