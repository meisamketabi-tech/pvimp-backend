from fastapi import APIRouter

from app.services.analytics_engine import engine

from app.services.statistics_service import service


router=APIRouter(
prefix="/analytics",
tags=["Analytics"]
)



@router.post("/summary")
def summary(data:list):

    return engine.summarize(data)



@router.post("/trend")
def trend(data:list):

    return service.trend(data)
