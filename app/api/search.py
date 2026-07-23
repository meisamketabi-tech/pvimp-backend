from fastapi import APIRouter

from app.services.search_service import service


router=APIRouter(
prefix="/search",
tags=["Search"]
)



@router.post("/index")
def index(data:dict):

    return service.index(data)



@router.get("/")
def search(keyword:str):

    return service.search(keyword)
