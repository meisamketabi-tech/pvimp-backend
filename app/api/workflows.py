from fastapi import APIRouter

from app.services.workflow_builder import builder


router=APIRouter(
prefix="/workflows",
tags=["Workflows"]
)



@router.post("/create")
def create(data:dict):

    return builder.create(data)



@router.post("/execute")
def execute(data:dict):

    return builder.execute(
        data.get("workflow"),
        data.get("action")
    )
