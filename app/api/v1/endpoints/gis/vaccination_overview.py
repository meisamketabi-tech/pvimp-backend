from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.services.gis.vaccination_overview_scope import overview
from app.services.gis.vaccination_overview_fast import overview as vaccination_overview
from app.services.gis.vaccination_overview_service import DEFAULT_NEAR_EXPIRY_DAYS

router = APIRouter(prefix="/gis/kpi/vaccination", tags=["GIS Vaccination KPI"])

_GLOBAL_SCOPE_ROLES = {"admin", "director_general", "health_deputy", "مدیرکل دامپزشکی استان"}
_COUNTY_SCOPE_ROLES = {"county_head", "رئیس اداره"}


def _get_overview_scope(db: Session, user_id: int, requested_county: str | None):
    rows = db.execute(text("""
        SELECT LOWER(BTRIM(r.name)) AS role_name,
               ou.county_id,
               BTRIM(c.county_code) AS county_code
        FROM user_assignments ua
        JOIN roles r ON r.id = ua.role_id
        JOIN organization_units ou ON ou.id = ua.organization_unit_id
        LEFT JOIN gis_counties c ON c.id = ou.county_id AND c.is_active = TRUE
        WHERE ua.user_id = :user_id
          AND ua.is_active = TRUE
          AND r.is_active = TRUE
          AND ou.is_active = TRUE
    """), {"user_id": user_id}).mappings().all()

    if any(row["role_name"] in _GLOBAL_SCOPE_ROLES for row in rows):
        return requested_county, None

    allowed = {
        str(row["county_code"]).strip()
        for row in rows
        if row["role_name"] in _COUNTY_SCOPE_ROLES
        and row["county_id"] is not None
        and row["county_code"]
    }

    if not allowed:
        raise HTTPException(403, "No organizational county scope is assigned.")

    if requested_county:
        requested = str(requested_county).strip()
        if requested not in allowed:
            raise HTTPException(403, "You cannot access this county.")
        return requested, allowed

    return (next(iter(allowed)) if len(allowed) == 1 else None), allowed


@router.get("/overview")
def vaccination_overview(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    near_expiry_days: int = Query(DEFAULT_NEAR_EXPIRY_DAYS, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db.execute(text("SET LOCAL work_mem = '64MB'"))
    db.execute(text("SET LOCAL jit = off"))

    requested_scope, allowed_codes = _get_overview_scope(db, int(current_user.id), county_code)

    return vaccination_overview(
        db=db,
        province_code=province_code,
        county_code=requested_scope,
        allowed_county_codes=allowed_codes,
        near_expiry_days=near_expiry_days,
    )
