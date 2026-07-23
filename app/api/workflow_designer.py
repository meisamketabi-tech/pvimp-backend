from fastapi import APIRouter

from app.services.workflow_designer import designer


router=APIRouter(
prefix="/workflow-designer",
tags=["Workflow Designer"]
)



@router.post("/create")
def create(data:dict):

    return designer.create(data)



@router.post("/validate")
def validate(data:dict):

    return designer.validate(
        data
    )
