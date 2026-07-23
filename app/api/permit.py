
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.permit import Permit



router=APIRouter(
prefix="/permits",
tags=["Health Permits"]
)



@router.post("/")
def create_permit(
data:dict,
db:Session=Depends(get_db)
):

    obj=Permit(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/")
def list_permits(
db:Session=Depends(get_db)
):

    return db.query(
        Permit
    ).order_by(
        Permit.id.desc()
    ).all()




@router.get("/unit/{id}")
def unit_permits(
id:int,
db:Session=Depends(get_db)
):

    return db.query(
        Permit
    ).filter(
        Permit.unit_id==id
    ).all()

