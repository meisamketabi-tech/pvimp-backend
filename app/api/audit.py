from fastapi import APIRouter

from app.services.audit_service import service


router=APIRouter(
prefix="/audit",
tags=["Audit"]
)



@router.post("/record")
def record(data:dict):

    return service.record(data)



@router.get("/history")
def history():

    return service.history()
