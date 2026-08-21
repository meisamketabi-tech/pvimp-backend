from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.gis_vaccination_performance_service import (
    GISVaccinationPerformanceService,
)


router = APIRouter(
    prefix="/gis/vaccination-performances",
    tags=["GIS Vaccination Performance"],
)


# ============================================================
# 1. وضعیت کلی یک واکسن
#    Vaccine -> Province -> Counties -> Units
# ============================================================

@router.get("/vaccine/{vaccine_type}/summary")
def get_vaccine_summary(
    vaccine_type: str,
    province_code: Optional[str] = Query(
        default=None,
    ),
    db: Session = Depends(get_db),
):
    return GISVaccinationPerformanceService.get_vaccine_summary(
        db=db,
        vaccine=vaccine_type,
        province_code=province_code,
    )


# ============================================================
# 2. جزئیات شهرستان برای یک واکسن
#    Vaccine -> County -> Units
# ============================================================

@router.get("/vaccine/{vaccine_type}/county/{county_code}")
def get_vaccine_county_details(
    vaccine_type: str,
    county_code: str,
    db: Session = Depends(get_db),
):
    result = GISVaccinationPerformanceService.get_county_details(
        db=db,
        vaccine=vaccine_type,
        county_code=county_code,
    )

    return result


# ============================================================
# 3. وضعیت یک واحد برای یک واکسن
#    Vaccine -> County -> Unit
# ============================================================

@router.get(
    "/vaccine/{vaccine_type}/unit/{epidemiology_unit_id}"
)
def get_vaccine_unit_details(
    vaccine_type: str,
    epidemiology_unit_id: int,
    db: Session = Depends(get_db),
):
    result = GISVaccinationPerformanceService.get_unit_details(
        db=db,
        vaccine=vaccine_type,
        epidemiology_unit_id=epidemiology_unit_id,
    )

    if not result.get("operations"):
        raise HTTPException(
            status_code=404,
            detail="Vaccination performance history not found.",
        )

    return result