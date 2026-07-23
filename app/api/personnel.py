
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.personnel import HealthPersonnel



router=APIRouter(
prefix="/personnel",
tags=["Health Personnel"]
)



@router.post("/")
def create_person(
data:dict,
db:Session=Depends(get_db)
):

    obj=HealthPersonnel(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/")
def list_personnel(
db:Session=Depends(get_db)
):

    return db.query(
        HealthPersonnel
    ).all()

