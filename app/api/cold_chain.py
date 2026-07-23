
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.cold_chain import ColdChainLog



router=APIRouter(
prefix="/cold-chain",
tags=["Cold Chain"]
)



@router.post("/")
def create_log(
data:dict,
db:Session=Depends(get_db)
):

    obj=ColdChainLog(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/")
def list_logs(
db:Session=Depends(get_db)
):

    return db.query(
        ColdChainLog
    ).order_by(
        ColdChainLog.id.desc()
    ).all()




@router.get("/alerts")
def alerts(
db:Session=Depends(get_db)
):

    return db.query(
        ColdChainLog
    ).filter(
        ColdChainLog.status=="هشدار"
    ).all()

