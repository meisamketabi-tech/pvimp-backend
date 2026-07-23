
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.responsible_health import *


router=APIRouter(
prefix="/responsible-health",
tags=["Responsible Health"]
)



@router.get("/statistics")
def statistics(
db:Session=Depends(get_db)
):

    return {

        "officers":
        db.query(ResponsibleOfficer).count(),

        "inspections":
        db.query(Inspection).count(),

        "nonconformities":
        db.query(NonConformity).count(),

        "corrective_actions":
        db.query(CorrectiveAction).count(),

        "samples":
        db.query(Sampling).count(),

        "cold_chain_logs":
        db.query(ColdChainLog).count()

    }



@router.get("/officer/{id}/summary")
def officer_summary(
id:int,
db:Session=Depends(get_db)
):

    return {

        "officer_id":id,

        "inspections":
        db.query(Inspection)
        .filter(
            Inspection.officer_id==id
        ).count(),


        "violations":
        db.query(NonConformity)
        .filter(
            NonConformity.officer_id==id
        ).count(),


        "samples":
        db.query(Sampling).count()

    }



@router.get("/compliance-score/{id}")
def compliance_score(
id:int,
db:Session=Depends(get_db)
):

    total = db.query(NonConformity)\
    .filter(
        NonConformity.officer_id==id
    ).count()


    if total==0:
        score=100

    else:
        score=max(
            0,
            100-(total*10)
        )


    return {

        "officer_id":id,

        "compliance_score":score

    }

