
from fastapi import APIRouter,Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.score import HealthScore



router=APIRouter(
prefix="/scores",
tags=["Health Scores"]
)



@router.post("/")
def create_score(
data:dict,
db:Session=Depends(get_db)
):

    obj=HealthScore(
        **data
    )


    db.add(obj)

    db.commit()

    db.refresh(obj)


    return obj




@router.get("/")
def get_scores(
db:Session=Depends(get_db)
):

    return db.query(
        HealthScore
    ).order_by(
        HealthScore.final_score.desc()
    ).all()



@router.get("/{unit_id}")
def get_unit_score(
unit_id:int,
db:Session=Depends(get_db)
):

    return db.query(
        HealthScore
    ).filter(
        HealthScore.unit_id==unit_id
    ).first()

