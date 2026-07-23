from fastapi import APIRouter


router=APIRouter(
prefix="/inspection-plans",
tags=["Inspection Plans"]
)


@router.get("/")
def plans():

    return []


@router.post("/generate")
def generate(data:dict):

    return {
        "generated":True,
        "plan":data
    }
