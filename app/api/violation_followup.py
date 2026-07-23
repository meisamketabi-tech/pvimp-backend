
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.violation_followup import ViolationFollowUp



router=APIRouter(
prefix="/violation-followups",
tags=["Violation Follow Up"]
)



@router.post("/")
def create_followup(
data:dict,
db:Session=Depends(get_db)
):

    obj=ViolationFollowUp(
        **data
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/{violation_id}")
def get_followups(
violation_id:int,
db:Session=Depends(get_db)
):

    return db.query(
        ViolationFollowUp
    ).filter(
        ViolationFollowUp.violation_id==violation_id
    ).all()

