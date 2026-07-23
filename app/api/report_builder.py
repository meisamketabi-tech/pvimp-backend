from fastapi import APIRouter

from app.services.report_builder import builder

from app.services.export_service import service


router=APIRouter(
prefix="/report-builder",
tags=["Report Builder"]
)



@router.post("/create")
def create(data:dict):

    return builder.create(
        data.get("template"),
        data.get("data")
    )



@router.post("/export/pdf")
def pdf(data:dict):

    return service.pdf(data)



@router.post("/export/excel")
def excel(data:dict):

    return service.excel(data)
