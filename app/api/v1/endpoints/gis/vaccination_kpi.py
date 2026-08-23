from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_allowed_county_ids
from app.db.session import get_db
from app.services.gis.unit_history_service import unit_history
from app.services.gis.vaccination_kpi_service import (
    alerts, counties, dashboard, effectiveness, vaccine_county_report,
    vaccine_management_report, vaccine_unit_report,
    vaccine_unit_report_paginated, unit_detail, units, vaccines,
    county_units_report,
)

router = APIRouter(prefix="/gis/kpi/vaccination", tags=["GIS Vaccination KPI"])


def _get_allowed_county_codes(db: Session, allowed_county_ids: set[int] | None) -> set[str] | None:
    if allowed_county_ids is None:
        return None
    if not allowed_county_ids:
        return set()
    rows = db.execute(text("""
        SELECT county_code FROM gis_counties
        WHERE id = ANY(:county_ids) AND is_active = TRUE
    """), {"county_ids": list(allowed_county_ids)}).scalars().all()
    return {str(code).strip() for code in rows if code is not None}


def _authorize_county_code(db: Session, current_user, county_code: str) -> None:
    allowed = get_allowed_county_ids(db, current_user)
    if allowed is None:
        return
    codes = _get_allowed_county_codes(db, allowed)
    if not codes:
        raise HTTPException(403, "No organizational county scope is assigned.")
    if str(county_code).strip() not in codes:
        raise HTTPException(403, "You cannot access this county.")


def _resolve_county_scope(db: Session, current_user, requested: str | None) -> str | None:
    allowed = get_allowed_county_ids(db, current_user)
    if allowed is None:
        return requested
    codes = _get_allowed_county_codes(db, allowed)
    if not codes:
        raise HTTPException(403, "No organizational county scope is assigned.")
    if requested:
        if requested not in codes:
            raise HTTPException(403, "You cannot access this county.")
        return requested
    return next(iter(codes)) if len(codes) == 1 else None


def _authorize_unit_county(db: Session, current_user, unit_code: str) -> None:
    unit = db.execute(text("""
        SELECT county_id FROM gis_epidemiology_units
        WHERE unit_code = :unit_code LIMIT 1
    """), {"unit_code": str(unit_code).strip()}).mappings().first()
    if not unit:
        raise HTTPException(404, "Epidemiology unit not found.")
    if unit["county_id"] is None:
        raise HTTPException(403, "Epidemiology unit has no county scope.")
    county = db.execute(text("""
        SELECT county_code FROM gis_counties WHERE id = :county_id LIMIT 1
    """), {"county_id": int(unit["county_id"])}).mappings().first()
    if not county or not county["county_code"]:
        raise HTTPException(403, "Epidemiology unit county not found.")
    _authorize_county_code(db, current_user, str(county["county_code"]).strip())


@router.get("/dashboard")
def vaccination_dashboard(province_code: str | None = Query(None), county_code: str | None = Query(None), vaccine_type: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return dashboard(db, province_code, _resolve_county_scope(db, current_user, county_code), vaccine_type)


@router.get("/counties")
def vaccination_counties(province_code: str | None = Query(None), vaccine_type: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = counties(db, province_code, vaccine_type)
    allowed = get_allowed_county_ids(db, current_user)
    if allowed is None:
        return result
    codes = _get_allowed_county_codes(db, allowed)
    return [r for r in result if str(r.get("county_code", "")).strip() in codes]


@router.get("/vaccines")
def vaccination_vaccines(province_code: str | None = Query(None), county_code: str | None = Query(None), vaccine_type: str | None = Query(None), unit_code: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    county_code = _resolve_county_scope(db, current_user, county_code)
    if unit_code:
        _authorize_unit_county(db, current_user, unit_code)
    return vaccines(db, province_code, county_code, vaccine_type, unit_code)


@router.get("/units")
def vaccination_units(province_code: str | None = Query(None), county_code: str | None = Query(None), vaccine_type: str | None = Query(None), unit_code: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    county_code = _resolve_county_scope(db, current_user, county_code)
    if unit_code:
        _authorize_unit_county(db, current_user, unit_code)
    return units(db, province_code, county_code, vaccine_type, unit_code)


@router.get("/alerts")
def vaccination_alerts(province_code: str | None = Query(None), vaccine_type: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = alerts(db, province_code, vaccine_type)
    allowed = get_allowed_county_ids(db, current_user)
    if allowed is None:
        return result
    codes = _get_allowed_county_codes(db, allowed)
    return [r for r in result if str(r.get("county_code", "")).strip() in codes]


@router.get("/effectiveness")
def vaccination_effectiveness(province_code: str | None = Query(None), county_code: str | None = Query(None), vaccine_type: str | None = Query(None), unit_code: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    county_code = _resolve_county_scope(db, current_user, county_code)
    if unit_code:
        _authorize_unit_county(db, current_user, unit_code)
    return effectiveness(db, province_code, county_code, vaccine_type, unit_code)


@router.get("/unit/{unit_code}")
def vaccination_unit_detail(unit_code: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _authorize_unit_county(db, current_user, unit_code)
    return unit_detail(db, unit_code)


@router.get("/vaccine/{vaccine_type}/counties")
def vaccination_vaccine_counties(vaccine_type: str, province_code: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = vaccine_county_report(db, vaccine_type, province_code)
    allowed = get_allowed_county_ids(db, current_user)
    if allowed is None:
        return result
    codes = _get_allowed_county_codes(db, allowed)
    return [r for r in result if str(r.get("county_code", "")).strip() in codes]


@router.get("/vaccine/{vaccine_type}/units")
def vaccination_vaccine_units(vaccine_type: str, province_code: str | None = Query(None), county_code: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    county_code = _resolve_county_scope(db, current_user, county_code)
    return vaccine_unit_report(db, vaccine_type, province_code, county_code)


@router.get("/vaccine/{vaccine_type}/units-paginated")
def vaccination_vaccine_units_paginated(vaccine_type: str, province_code: str | None = Query(None), county_code: str | None = Query(None), page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    county_code = _resolve_county_scope(db, current_user, county_code)
    return vaccine_unit_report_paginated(db, vaccine_type, province_code, county_code, page, page_size)


@router.get("/county/{county_code}/units")
def vaccination_county_units(county_code: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    _authorize_county_code(db, current_user, county_code)
    row = db.execute(text("SELECT id FROM gis_counties WHERE county_code = :county_code LIMIT 1"), {"county_code": county_code}).mappings().first()
    if not row:
        raise HTTPException(404, "County not found.")
    return county_units_report(db=db, county_id=int(row["id"]))


@router.get("/unit/{unit_code}/history")
def vaccination_unit_history(unit_code: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    unit = db.execute(text("SELECT unit_code, county_id FROM gis_epidemiology_units WHERE unit_code = :unit_code LIMIT 1"), {"unit_code": str(unit_code).strip()}).mappings().first()
    if not unit:
        raise HTTPException(404, "Epidemiology unit not found.")
    if unit["county_id"] is not None:
        county = db.execute(text("SELECT county_code FROM gis_counties WHERE id = :id LIMIT 1"), {"id": int(unit["county_id"])}).mappings().first()
        if county and county["county_code"]:
            _authorize_county_code(db, current_user, str(county["county_code"]).strip())
    return unit_history(db, str(unit_code).strip())


@router.get("/management-report")
def vaccination_management_report(province_code: str | None = Query(None), county_code: str | None = Query(None), vaccine_type: str | None = Query(None), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    county_code = _resolve_county_scope(db, current_user, county_code)
    return vaccine_management_report(db=db, province_code=province_code, county_code=county_code, vaccine_type=vaccine_type)
