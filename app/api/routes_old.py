from fastapi import APIRouter

from app.services.route_optimizer import engine


router=APIRouter(
prefix="/routes",
tags=["Inspection Routes"]
)



@router.post("/optimize")
def optimize(data:list):

    return engine.optimize(data)



@router.get("/")
def list_routes():

    return []
