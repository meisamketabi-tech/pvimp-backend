
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.responsible_health_unit import ResponsibleHealthUnit



router=APIRouter(
prefix="/health-units",
tags=["Responsible Health Units"]
)



@router.post("/")
def create_unit(
data:dict,
db:Session=Depends(get_db)
):

    obj=ResponsibleHealthUnit(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/")
def list_units(
db:Session=Depends(get_db)
):

    return db.query(
        ResponsibleHealthUnit
    ).all()

