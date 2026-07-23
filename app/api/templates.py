from fastapi import APIRouter

from app.services.template_service import service


router=APIRouter(
prefix="/templates",
tags=["Templates"]
)



@router.post("/")
def create(data:dict):

    return service.create(data)



@router.post("/render")
def render(data:dict):

    return service.render(
        data.get("template"),
        data.get("values")
    )
