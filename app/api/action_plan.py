
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.action_plan import CorrectiveActionPlan



router=APIRouter(
prefix="/actions",
tags=["Corrective Actions"]
)



@router.post("/")
def create_action(
data:dict,
db:Session=Depends(get_db)
):

    obj=CorrectiveActionPlan(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/")
def list_actions(
db:Session=Depends(get_db)
):

    return db.query(
        CorrectiveActionPlan
    ).all()




@router.put("/{id}/complete")
def complete_action(
id:int,
db:Session=Depends(get_db)
):

    obj=db.query(
        CorrectiveActionPlan
    ).filter(
        CorrectiveActionPlan.id==id
    ).first()


    obj.completed=True

    obj.status="انجام شده"


    db.commit()


    return obj

