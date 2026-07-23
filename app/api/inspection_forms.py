from fastapi import APIRouter

from app.services.inspection_form_engine import engine


router=APIRouter(
prefix="/inspection-forms",
tags=["Inspection Forms"]
)



@router.post("/validate")
def validate(data:dict):

    return engine.validate(
        data.get("schema",[]),
        data.get("values",{})
    )



@router.post("/render")
def render(data:dict):

    return engine.build(
        data.get("schema","[]")
    )
