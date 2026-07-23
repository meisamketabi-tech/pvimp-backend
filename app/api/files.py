from fastapi import APIRouter

from app.services.file_service import service


router=APIRouter(
prefix="/files",
tags=["Files"]
)



@router.post("/upload")
def upload(data:dict):

    return service.upload(data)



@router.get("/{entity}/{id}")
def files(
    entity:str,
    id:int
):

    return service.list_files(
        entity,
        id
    )
