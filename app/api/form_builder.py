from fastapi import APIRouter

router=APIRouter(
prefix="/form-builder",
tags=["Form Builder"]
)


@router.get("/")
def forms():

    return []


@router.get("/{id}")
def form(id:int):

    return {
        "id":id,
        "fields":[]
    }


@router.post("/submit")
def submit(data:dict):

    return {
        "saved":True,
        "data":data
    }
