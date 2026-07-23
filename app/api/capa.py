from fastapi import APIRouter


router=APIRouter(
prefix="/capa",
tags=["CAPA"]
)


@router.get("/")
def list_actions():

    return []


@router.post("/")
def create(data:dict):

    return data
