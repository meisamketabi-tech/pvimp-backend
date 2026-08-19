from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.gis.live_dashboard_kpi_service_v2 import (
    LiveDashboardKPIServiceV2,
)


ZANJAN_PROVINCE_ID = 5

router = APIRouter(
    prefix="/gis/dashboard/kpi-v2",
    tags=["GIS Live KPI Dashboard V2"],
)


@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
):
    return LiveDashboardKPIServiceV2(db).overview()


@router.get("/provinces")
def provinces(
    metric: str = "all",
    db: Session = Depends(get_db),
):
    return {
        "metric": metric,
        "items":
            LiveDashboardKPIServiceV2(db)
            .provinces(metric)
    }


@router.get("/provinces/{province_id}/counties")
def counties(
    province_id: int,
    metric: str = "all",
    db: Session = Depends(get_db),
):
    return {
        "province_id": province_id,
        "metric": metric,
        "items":
            LiveDashboardKPIServiceV2(db)
            .counties(
                province_id,
                metric
            )
    }


@router.get("/counties/{county_id}/units")
def units(
    county_id: int,
    metric: str = "all",
    db: Session = Depends(get_db),
):
    return {
        "county_id": county_id,
        "metric": metric,
        "items":
            LiveDashboardKPIServiceV2(db)
            .units(
                county_id,
                metric
            )
    }


@router.get("/units/{unit_id}")
def unit_detail(
    unit_id: int,
    db: Session = Depends(get_db),
):
    return LiveDashboardKPIServiceV2(db).unit_detail(
        unit_id
    )


@router.get("/units/{unit_id}/chain")
def unit_chain(
    unit_id: int,
    operation_id: int | None = None,
    db: Session = Depends(get_db),
):
    return {
        "unit_id": unit_id,
        "operation_id": operation_id,
        "items":
            LiveDashboardKPIServiceV2(db)
            .related_chain(
                unit_id,
                operation_id
            )
    }