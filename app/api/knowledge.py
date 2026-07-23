from fastapi import APIRouter

from app.services.search_engine import engine

from app.services.knowledge_service import service


router=APIRouter(
prefix="/knowledge",
tags=["Knowledge Base"]
)



@router.post("/search")
def search(data:dict):

    return engine.search(
        data.get("keyword")
    )



@router.post("/")
def add(data:dict):

    return service.add(data)
