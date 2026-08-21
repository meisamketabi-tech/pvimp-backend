from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_user,
    get_allowed_county_ids,
)

from app.db.session import get_db

from app.services.gis.vaccination_kpi_service import (
    alerts,
    counties,
    dashboard,
    effectiveness,
    vaccine_county_report,
    vaccine_management_report,
    vaccine_unit_report,
    vaccine_unit_report_paginated,
    unit_detail,
    units,
    vaccines,
    county_units_report,
)

router = APIRouter(
    prefix="/gis/kpi/vaccination",
    tags=["GIS Vaccination KPI"],
)


# =========================================================
# Scope helpers
# =========================================================


def _get_allowed_county_codes(
    db: Session,
    allowed_county_ids: set[int] | None,
) -> set[str] | None:
    """
    None:
        global access

    empty set:
        no access

    set[str]:
        allowed county codes
    """

    if allowed_county_ids is None:
        return None

    if not allowed_county_ids:
        return set()

    rows = (
        db.execute(
            text("""
                SELECT county_code
                FROM gis_counties
                WHERE id = ANY(:county_ids)
                AND is_active = TRUE
                """),
            {
                "county_ids": list(allowed_county_ids),
            },
        )
        .scalars()
        .all()
    )

    return {str(code).strip() for code in rows if code is not None}


def _authorize_county_code(
    db: Session,
    current_user,
    county_code: str,
) -> None:

    allowed_county_ids = get_allowed_county_ids(
        db,
        current_user,
    )

    if allowed_county_ids is None:
        return

    allowed_codes = _get_allowed_county_codes(
        db,
        allowed_county_ids,
    )

    if not allowed_codes:
        raise HTTPException(
            status_code=403,
            detail="No organizational county scope is assigned.",
        )

    if county_code not in allowed_codes:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this county.",
        )


def _resolve_county_scope(
    db: Session,
    current_user,
    requested_county_code: str | None,
) -> str | None:

    allowed_county_ids = get_allowed_county_ids(
        db,
        current_user,
    )

    if allowed_county_ids is None:
        return requested_county_code

    allowed_codes = _get_allowed_county_codes(
        db,
        allowed_county_ids,
    )

    if not allowed_codes:
        raise HTTPException(
            status_code=403,
            detail="No organizational county scope is assigned.",
        )

    if requested_county_code:

        if requested_county_code not in allowed_codes:
            raise HTTPException(
                status_code=403,
                detail="You cannot access this county.",
            )

        return requested_county_code

    if len(allowed_codes) == 1:
        return next(iter(allowed_codes))

    return None


# =========================================================
# Dashboard
# =========================================================


@router.get("/dashboard")
def vaccination_dashboard(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    county_code = _resolve_county_scope(
        db,
        current_user,
        county_code,
    )

    return dashboard(
        db,
        province_code=province_code,
        county_code=county_code,
        vaccine_type=vaccine_type,
    )


# =========================================================
# Counties
# =========================================================


@router.get("/counties")
def vaccination_counties(
    province_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    result = counties(
        db,
        province_code=province_code,
        vaccine_type=vaccine_type,
    )

    allowed_county_ids = get_allowed_county_ids(
        db,
        current_user,
    )

    if allowed_county_ids is None:
        return result

    allowed_codes = _get_allowed_county_codes(
        db,
        allowed_county_ids,
    )

    return [
        row
        for row in result
        if str(row.get("county_code", "")).strip() in allowed_codes
    ]


# =========================================================
# Vaccines
# =========================================================


@router.get("/vaccines")
def vaccination_vaccines(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    unit_code: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    county_code = _resolve_county_scope(
        db,
        current_user,
        county_code,
    )

    return vaccines(
        db,
        province_code=province_code,
        county_code=county_code,
        vaccine_type=vaccine_type,
        unit_code=unit_code,
    )


# =========================================================
# Units
# =========================================================


@router.get("/units")
def vaccination_units(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    unit_code: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    county_code = _resolve_county_scope(
        db,
        current_user,
        county_code,
    )

    return units(
        db,
        province_code=province_code,
        county_code=county_code,
        vaccine_type=vaccine_type,
        unit_code=unit_code,
    )


# =========================================================
# Alerts
# =========================================================


@router.get("/alerts")
def vaccination_alerts(
    province_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    result = alerts(
        db,
        province_code=province_code,
        vaccine_type=vaccine_type,
    )

    allowed_county_ids = get_allowed_county_ids(
        db,
        current_user,
    )

    if allowed_county_ids is None:
        return result

    allowed_codes = _get_allowed_county_codes(
        db,
        allowed_county_ids,
    )

    return [
        row
        for row in result
        if str(row.get("county_code", "")).strip() in allowed_codes
    ]


# =========================================================
# Effectiveness
# =========================================================


@router.get("/effectiveness")
def vaccination_effectiveness(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    unit_code: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    county_code = _resolve_county_scope(
        db,
        current_user,
        county_code,
    )

    return effectiveness(
        db,
        province_code=province_code,
        county_code=county_code,
        vaccine_type=vaccine_type,
        unit_code=unit_code,
    )


# =========================================================
# Unit Detail
# =========================================================


@router.get("/unit/{unit_code}")
def vaccination_unit_detail(
    unit_code: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return unit_detail(
        db,
        unit_code,
    )


# =========================================================
# Vaccine / Counties
# =========================================================


@router.get("/vaccine/{vaccine_type}/counties")
def vaccination_vaccine_counties(
    vaccine_type: str,
    province_code: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    result = vaccine_county_report(
        db,
        vaccine_type,
        province_code,
    )

    allowed_county_ids = get_allowed_county_ids(
        db,
        current_user,
    )

    if allowed_county_ids is None:
        return result

    allowed_codes = _get_allowed_county_codes(
        db,
        allowed_county_ids,
    )

    return [
        row
        for row in result
        if str(
            row.get(
                "county_code",
                "",
            )
        ).strip()
        in allowed_codes
    ]


# =========================================================
# Vaccine / Units
# =========================================================


@router.get("/vaccine/{vaccine_type}/units")
def vaccination_vaccine_units(
    vaccine_type: str,
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    county_code = _resolve_county_scope(
        db,
        current_user,
        county_code,
    )

    return vaccine_unit_report(
        db,
        vaccine_type,
        province_code,
        county_code,
    )


# =========================================================
# Vaccine / Units Pagination
# =========================================================


@router.get("/vaccine/{vaccine_type}/units-paginated")
def vaccination_vaccine_units_paginated(
    vaccine_type: str,
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    page: int = Query(
        1,
        ge=1,
    ),
    page_size: int = Query(
        50,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    county_code = _resolve_county_scope(
        db,
        current_user,
        county_code,
    )

    return vaccine_unit_report_paginated(
        db=db,
        vaccine_type=vaccine_type,
        province_code=province_code,
        county_code=county_code,
        page=page,
        page_size=page_size,
    )


# =========================================================
# County Drilldown
#
# county_code is business code
# NOT gis_counties.id
# =========================================================


@router.get("/county/{county_code}/units")
def vaccination_county_units(
    county_code: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    _authorize_county_code(
        db,
        current_user,
        county_code,
    )

    county_row = (
        db.execute(
            text("""
                SELECT id

                FROM gis_counties

                WHERE county_code = :county_code

                LIMIT 1
                """),
            {
                "county_code": county_code,
            },
        )
        .mappings()
        .first()
    )

    if not county_row:

        raise HTTPException(
            status_code=404,
            detail="County not found.",
        )

    return county_units_report(
        db=db,
        county_id=int(county_row["id"]),
    )


# =========================================================
# Management Report
# =========================================================


@router.get("/management-report")
def vaccination_management_report(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    county_code = _resolve_county_scope(
        db,
        current_user,
        county_code,
    )

    return vaccine_management_report(
        db=db,
        province_code=province_code,
        county_code=county_code,
        vaccine_type=vaccine_type,
    )
