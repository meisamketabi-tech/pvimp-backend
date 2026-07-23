
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.health_alert import HealthAlert



router=APIRouter(
prefix="/alerts",
tags=["Health Alerts"]
)



@router.post("/")
def create_alert(
data:dict,
db:Session=Depends(get_db)
):

    obj=HealthAlert(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/")
def list_alerts(
db:Session=Depends(get_db)
):

    return db.query(
        HealthAlert
    ).order_by(
        HealthAlert.id.desc()
    ).all()




@router.put("/{id}")
def update_alert(
id:int,
status:str,
db:Session=Depends(get_db)
):

    obj=db.query(
        HealthAlert
    ).filter(
        HealthAlert.id==id
    ).first()


    obj.status=status

    db.commit()


    return obj

