from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_allowed_county_ids, get_current_user
from app.db.session import get_db
from app.services.gis.vaccination_overview_service import (
    DEFAULT_NEAR_EXPIRY_DAYS,
    overview,
)
from app.api.v1.endpoints.gis.vaccination_kpi import _get_allowed_county_codes, _resolve_county_scope

router = APIRouter(prefix="/gis/kpi/vaccination", tags=["GIS Vaccination KPI"])


@router.get("/overview")
def vaccination_overview(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    near_expiry_days: int = Query(DEFAULT_NEAR_EXPIRY_DAYS, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    requested_scope = _resolve_county_scope(db, current_user, county_code)
    allowed = get_allowed_county_ids(db, current_user)
    allowed_codes = _get_allowed_county_codes(db, allowed) if allowed is not None else None
    return overview(
        db=db,
        province_code=province_code,
        county_code=requested_scope,
        allowed_county_codes=allowed_codes,
        near_expiry_days=near_expiry_days,
    )
