from fastapi import APIRouter

from app.services.workflow_runtime import runtime


router=APIRouter(
prefix="/workflow-runtime",
tags=["Workflow Runtime"]
)



@router.post("/move")
def move(data:dict):

    return runtime.move(
        data.get("current"),
        data.get("target")
    )
