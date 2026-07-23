from fastapi import APIRouter

from app.services.inventory_service import service


router=APIRouter(
prefix="/inventory",
tags=["Inventory"]
)



@router.post("/")
def add(data:dict):

    return service.add(data)



@router.get("/stock")
def stock():

    return service.stock()
