from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.gis.live_dashboard_kpi_service import (
    LiveDashboardKPIService,
)

router = APIRouter(
    prefix="/gis/dashboard/kpi",
    tags=["GIS Dashboard KPI"],
)


# =========================================================
# Overview
# =========================================================


@router.get("/overview")
def dashboard_overview(
    start: date | None = Query(None),
    end: date | None = Query(None),
    db: Session = Depends(get_db),
):
    service = LiveDashboardKPIService(db)

    return service.overview(
        start=start,
        end=end,
    )


# =========================================================
# Unit detail
# =========================================================


@router.get("/units/{unit_id}")
def dashboard_unit(
    unit_id: int,
    db: Session = Depends(get_db),
):
    service = LiveDashboardKPIService(db)

    return service.unit_detail(unit_id)


# =========================================================
# County detail
# =========================================================


@router.get("/counties/{county_id}")
def dashboard_county(
    county_id: int,
    db: Session = Depends(get_db),
):
    service = LiveDashboardKPIService(db)

    return service.county_detail(county_id)


# =========================================================
# KPI drilldown
# =========================================================


@router.get("/drilldown/{metric}")
def dashboard_metric_drilldown(
    metric: str,
    db: Session = Depends(get_db),
):
    allowed_metrics = {
        "all",
        "vaccination",
        "disease_reports",
        "care",
        "lab",
        "samples",
        "spraying",
        "operations",
    }

    normalized_metric = metric.strip().lower()

    if normalized_metric not in allowed_metrics:
        return {
            "metric": metric,
            "units": [],
            "error": "unsupported metric",
        }

    service = LiveDashboardKPIService(db)

    return {
        "metric": normalized_metric,
        "units": service.metric_units(normalized_metric),
    }


# =========================================================
# Map
# =========================================================


@router.get("/map")
def dashboard_map(
    db: Session = Depends(get_db),
):
    service = LiveDashboardKPIService(db)

    return {
        "live": True,
        "points": service.map_points(),
    }
