
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.training import HealthTraining



router=APIRouter(
prefix="/trainings",
tags=["Trainings"]
)



@router.post("/")
def create_training(
data:dict,
db:Session=Depends(get_db)
):

    obj=HealthTraining(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/")
def list_training(
db:Session=Depends(get_db)
):

    return db.query(
        HealthTraining
    ).order_by(
        HealthTraining.id.desc()
    ).all()

