
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.approval import ApprovalRequest



router=APIRouter(
prefix="/approval",
tags=["Approval Workflow"]
)



@router.post("/")
def create_request(
data:dict,
db:Session=Depends(get_db)
):

    obj=ApprovalRequest(
        **data
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj




@router.get("/")
def get_requests(
db:Session=Depends(get_db)
):

    return db.query(
        ApprovalRequest
    ).order_by(
        ApprovalRequest.id.desc()
    ).all()




@router.put("/{id}")
def review(
id:int,
status:str,
comment:str="",
db:Session=Depends(get_db)
):

    obj=db.query(
        ApprovalRequest
    ).filter(
        ApprovalRequest.id==id
    ).first()


    obj.status=status

    obj.comment=comment


    db.commit()


    return obj

