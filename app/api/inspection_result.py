
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.inspection_result import InspectionResult



router=APIRouter(
prefix="/inspection-results",
tags=["Inspection Results"]
)



@router.post("/")
def create_result(
data:dict,
db:Session=Depends(get_db)
):

    obj=InspectionResult(
        **data
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj




@router.get("/{inspection_id}")
def get_results(
inspection_id:int,
db:Session=Depends(get_db)
):

    return db.query(
        InspectionResult
    ).filter(
        InspectionResult.inspection_id==inspection_id
    ).all()

