from fastapi import APIRouter


router=APIRouter(
prefix="/complaints",
tags=["Complaints"]
)


@router.get("/")
def complaints():

    return []


@router.post("/")
def register(data:dict):

    return data
