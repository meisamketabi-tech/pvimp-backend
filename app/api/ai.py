from fastapi import APIRouter

from app.services.ai_service import service


router=APIRouter(
prefix="/ai",
tags=["AI"]
)



@router.post("/analyze")
def analyze(data:dict):

    return service.analyze(data)



@router.post("/predict")
def predict(data:dict):

    return service.predict(data)
