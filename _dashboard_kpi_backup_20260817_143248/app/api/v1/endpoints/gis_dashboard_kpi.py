from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.gis.live_dashboard_kpi_service import LiveDashboardKPIService

router = APIRouter(prefix="/gis/dashboard/kpi", tags=["GIS Dashboard KPI"])


@router.get("/overview")
def dashboard_overview(
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    return LiveDashboardKPIService(db).overview(start, end)


@router.get("/units/{unit_id}")
def dashboard_unit(unit_id: int, db: Session = Depends(get_db)):
    return LiveDashboardKPIService(db).unit_detail(unit_id)


@router.get("/counties/{county_id}")
def dashboard_county(county_id: int, db: Session = Depends(get_db)):
    return LiveDashboardKPIService(db).county_detail(county_id)


@router.get("/drilldown/{metric}")
def dashboard_metric_drilldown(metric: str, db: Session = Depends(get_db)):
    allowed = {"all","vaccination","disease_reports","care","lab","samples","spraying","operations"}
    if metric not in allowed:
        return {"metric": metric, "units": [], "error": "unsupported metric"}
    return {"metric": metric, "units": LiveDashboardKPIService(db).metric_units(metric)}


@router.get("/map")
def dashboard_map(db: Session = Depends(get_db)):
    return {"live": True, "points": LiveDashboardKPIService(db).map_points()}