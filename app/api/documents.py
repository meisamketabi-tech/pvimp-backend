from fastapi import APIRouter

from app.services.document_service import service


router=APIRouter(
prefix="/documents",
tags=["Documents"]
)



@router.post("/upload")
def upload(data:dict):

    return service.upload(data)



@router.get("/")
def list():

    return service.list()



@router.delete("/{id}")
def delete(id:int):

    return service.delete(id)
