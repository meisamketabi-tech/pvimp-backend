
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.audit_log import AuditLog



router=APIRouter(
prefix="/audit",
tags=["Audit"]
)



@router.post("/")
def create_log(
data:dict,
db:Session=Depends(get_db)
):

    obj=AuditLog(
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
        AuditLog
    ).order_by(
        AuditLog.id.desc()
    ).all()

