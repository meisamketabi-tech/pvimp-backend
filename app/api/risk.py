from fastapi import APIRouter

from app.services.risk_engine import engine


router=APIRouter(
prefix="/risk",
tags=["Risk Assessment"]
)



@router.post("/calculate")
def calculate(data:dict):

    return engine.calculate(data)
