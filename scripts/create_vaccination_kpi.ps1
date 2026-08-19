$ErrorActionPreference = "Stop"

$Root = "D:\pvimp_backend"
Set-Location $Root

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    $dir = Split-Path $Path -Parent
    if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8)
}

# ============================================================
# 1) KPI service
# ============================================================
Write-Utf8NoBom "$Root\app\services\gis\vaccination_kpi_service.py" @'
from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


VACCINATION_TABLE = "gis_vaccination_performances"


def _filters(
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
    unit_code: str | None = None,
) -> tuple[str, dict[str, Any]]:
    clauses = []
    params: dict[str, Any] = {}

    if province_code:
        clauses.append("province_code = :province_code")
        params["province_code"] = province_code
    if county_code:
        clauses.append("county_code = :county_code")
        params["county_code"] = county_code
    if vaccine_type:
        clauses.append("vaccine_type = :vaccine_type")
        params["vaccine_type"] = vaccine_type
    if unit_code:
        clauses.append("epidemiology_unit_code = :unit_code")
        params["unit_code"] = unit_code

    return (" WHERE " + " AND ".join(clauses)) if clauses else "", params


def _pct(numerator: float | None, denominator: float | None) -> float:
    if not denominator:
        return 0.0
    return round((float(numerator or 0) / float(denominator)) * 100, 2)


def dashboard(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
) -> dict[str, Any]:
    where, params = _filters(province_code, county_code, vaccine_type)

    q = text(f"""
        SELECT
            COUNT(*) AS records,
            COALESCE(SUM(total_animals), 0) AS total_animals,
            COALESCE(SUM(eligible_animals), 0) AS eligible_animals,
            COALESCE(SUM(vaccinated_animals), 0) AS vaccinated_animals,
            COUNT(DISTINCT county_code) AS counties,
            COUNT(DISTINCT epidemiology_unit_code) AS units,
            COUNT(DISTINCT vaccine_type) AS vaccine_types,
            COALESCE(SUM(shock_count), 0) AS shock_count,
            COALESCE(SUM(death_count), 0) AS death_count,
            COALESCE(SUM(abortion_count), 0) AS abortion_count,
            COALESCE(SUM(hypersensitivity_count), 0) AS hypersensitivity_count,
            COALESCE(SUM(local_complication_count), 0) AS local_complication_count
        FROM {VACCINATION_TABLE}
        {where}
    """)
    row = db.execute(q, params).mappings().one()

    eligible = int(row["eligible_animals"] or 0)
    vaccinated = int(row["vaccinated_animals"] or 0)
    total = int(row["total_animals"] or 0)
    adverse = sum(
        int(row[k] or 0)
        for k in (
            "shock_count",
            "death_count",
            "abortion_count",
            "hypersensitivity_count",
            "local_complication_count",
        )
    )

    return {
        "records": int(row["records"] or 0),
        "total_animals": total,
        "eligible_animals": eligible,
        "vaccinated_animals": vaccinated,
        "coverage_percent": _pct(vaccinated, eligible or total),
        "remaining_animals": max((eligible or total) - vaccinated, 0),
        "counties": int(row["counties"] or 0),
        "units": int(row["units"] or 0),
        "vaccine_types": int(row["vaccine_types"] or 0),
        "adverse_events": adverse,
        "adverse_event_rate_percent": _pct(adverse, vaccinated),
        "side_effects": {
            "shock": int(row["shock_count"] or 0),
            "death_or_culling": int(row["death_count"] or 0),
            "abortion": int(row["abortion_count"] or 0),
            "hypersensitivity": int(row["hypersensitivity_count"] or 0),
            "local_complication": int(row["local_complication_count"] or 0),
        },
    }


def counties(
    db: Session,
    province_code: str | None = None,
    vaccine_type: str | None = None,
) -> list[dict[str, Any]]:
    where, params = _filters(province_code, None, vaccine_type)

    q = text(f"""
        SELECT
            county_code,
            MAX(county_name) AS county_name,
            COUNT(*) AS records,
            COUNT(DISTINCT epidemiology_unit_code) AS units,
            COALESCE(SUM(eligible_animals), 0) AS eligible_animals,
            COALESCE(SUM(vaccinated_animals), 0) AS vaccinated_animals,
            COALESCE(SUM(shock_count), 0) AS shock_count,
            COALESCE(SUM(death_count), 0) AS death_count,
            COALESCE(SUM(abortion_count), 0) AS abortion_count,
            COALESCE(SUM(hypersensitivity_count), 0) AS hypersensitivity_count,
            COALESCE(SUM(local_complication_count), 0) AS local_complication_count
        FROM {VACCINATION_TABLE}
        {where}
        GROUP BY county_code
        ORDER BY county_name NULLS LAST
    """)
    rows = db.execute(q, params).mappings().all()

    result = []
    for r in rows:
        eligible = int(r["eligible_animals"] or 0)
        vaccinated = int(r["vaccinated_animals"] or 0)
        adverse = sum(int(r[k] or 0) for k in (
            "shock_count", "death_count", "abortion_count",
            "hypersensitivity_count", "local_complication_count"
        ))
        coverage = _pct(vaccinated, eligible)
        status = "ON_TRACK"
        if coverage < 50:
            status = "CRITICAL"
        elif coverage < 75:
            status = "WARNING"

        result.append({
            "county_code": r["county_code"],
            "county_name": r["county_name"],
            "records": int(r["records"] or 0),
            "units": int(r["units"] or 0),
            "eligible_animals": eligible,
            "vaccinated_animals": vaccinated,
            "remaining_animals": max(eligible - vaccinated, 0),
            "coverage_percent": coverage,
            "adverse_events": adverse,
            "adverse_event_rate_percent": _pct(adverse, vaccinated),
            "status": status,
        })
    return result


def vaccines(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
) -> list[dict[str, Any]]:
    where, params = _filters(province_code, county_code)

    q = text(f"""
        SELECT
            vaccine_type,
            MAX(vaccine_brand) AS vaccine_brand,
            COUNT(*) AS records,
            COALESCE(SUM(eligible_animals), 0) AS eligible_animals,
            COALESCE(SUM(vaccinated_animals), 0) AS vaccinated_animals,
            COALESCE(SUM(shock_count), 0) AS shock_count,
            COALESCE(SUM(death_count), 0) AS death_count,
            COALESCE(SUM(abortion_count), 0) AS abortion_count,
            COALESCE(SUM(hypersensitivity_count), 0) AS hypersensitivity_count,
            COALESCE(SUM(local_complication_count), 0) AS local_complication_count
        FROM {VACCINATION_TABLE}
        {where}
        GROUP BY vaccine_type
        ORDER BY vaccine_type NULLS LAST
    """)
    rows = db.execute(q, params).mappings().all()

    return [
        {
            "vaccine_type": r["vaccine_type"],
            "vaccine_brand": r["vaccine_brand"],
            "records": int(r["records"] or 0),
            "eligible_animals": int(r["eligible_animals"] or 0),
            "vaccinated_animals": int(r["vaccinated_animals"] or 0),
            "coverage_percent": _pct(r["vaccinated_animals"], r["eligible_animals"]),
            "adverse_events": sum(int(r[k] or 0) for k in (
                "shock_count", "death_count", "abortion_count",
                "hypersensitivity_count", "local_complication_count"
            )),
            "adverse_event_rate_percent": _pct(
                sum(int(r[k] or 0) for k in (
                    "shock_count", "death_count", "abortion_count",
                    "hypersensitivity_count", "local_complication_count"
                )),
                r["vaccinated_animals"],
            ),
        }
        for r in rows
    ]


def units(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
) -> list[dict[str, Any]]:
    where, params = _filters(province_code, county_code, vaccine_type)

    q = text(f"""
        SELECT
            epidemiology_unit_code,
            MAX(epidemiology_unit_name) AS epidemiology_unit_name,
            MAX(province_name) AS province_name,
            MAX(county_name) AS county_name,
            MAX(epidemiology_unit_type) AS epidemiology_unit_type,
            COUNT(*) AS records,
            COALESCE(SUM(eligible_animals), 0) AS eligible_animals,
            COALESCE(SUM(vaccinated_animals), 0) AS vaccinated_animals,
            COALESCE(SUM(shock_count), 0) AS shock_count,
            COALESCE(SUM(death_count), 0) AS death_count,
            COALESCE(SUM(abortion_count), 0) AS abortion_count,
            COALESCE(SUM(hypersensitivity_count), 0) AS hypersensitivity_count,
            COALESCE(SUM(local_complication_count), 0) AS local_complication_count
        FROM {VACCINATION_TABLE}
        {where}
        GROUP BY epidemiology_unit_code
        ORDER BY county_name NULLS LAST, epidemiology_unit_name NULLS LAST
    """)
    rows = db.execute(q, params).mappings().all()

    result = []
    for r in rows:
        eligible = int(r["eligible_animals"] or 0)
        vaccinated = int(r["vaccinated_animals"] or 0)
        adverse = sum(int(r[k] or 0) for k in (
            "shock_count", "death_count", "abortion_count",
            "hypersensitivity_count", "local_complication_count"
        ))
        result.append({
            "unit_code": r["epidemiology_unit_code"],
            "unit_name": r["epidemiology_unit_name"],
            "province_name": r["province_name"],
            "county_name": r["county_name"],
            "unit_type": r["epidemiology_unit_type"],
            "records": int(r["records"] or 0),
            "eligible_animals": eligible,
            "vaccinated_animals": vaccinated,
            "remaining_animals": max(eligible - vaccinated, 0),
            "coverage_percent": _pct(vaccinated, eligible),
            "adverse_events": adverse,
            "adverse_event_rate_percent": _pct(adverse, vaccinated),
        })
    return result


def alerts(db: Session, province_code: str | None = None) -> list[dict[str, Any]]:
    result = []

    for row in counties(db, province_code=province_code):
        if row["coverage_percent"] < 50:
            result.append({
                "severity": "CRITICAL",
                "type": "LOW_COVERAGE",
                "county_code": row["county_code"],
                "county_name": row["county_name"],
                "message": "پوشش واکسیناسیون شهرستان کمتر از ۵۰ درصد است.",
                "details": row,
            })
        elif row["coverage_percent"] < 75:
            result.append({
                "severity": "WARNING",
                "type": "LOW_COVERAGE",
                "county_code": row["county_code"],
                "county_name": row["county_name"],
                "message": "پوشش واکسیناسیون شهرستان نیازمند پیگیری است.",
                "details": row,
            })

        if row["adverse_event_rate_percent"] >= 1:
            result.append({
                "severity": "HIGH",
                "type": "ADVERSE_EVENT_RATE",
                "county_code": row["county_code"],
                "county_name": row["county_name"],
                "message": "نرخ عوارض ثبت‌شده واکسیناسیون نیازمند بررسی است.",
                "details": row,
            })

    return result


def effectiveness(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    vaccine_type: str | None = None,
) -> dict[str, Any]:
    where, params = _filters(province_code, county_code, vaccine_type)

    vaccination = db.execute(text(f"""
        SELECT
            COUNT(DISTINCT epidemiology_unit_code) AS vaccinated_units,
            COALESCE(SUM(vaccinated_animals), 0) AS vaccinated_animals,
            COALESCE(SUM(shock_count), 0) AS adverse_events
        FROM {VACCINATION_TABLE}
        {where}
    """), params).mappings().one()

    disease_where = []
    disease_params = dict(params)
    if province_code:
        disease_where.append("d.province_name = :province_code")
    if county_code:
        disease_where.append("d.county_name = :county_code")

    disease_clause = (" WHERE " + " AND ".join(disease_where)) if disease_where else ""

    # Conservative analytical signal: disease after vaccination is reported as
    # an association requiring investigation, not as proof of vaccine failure.
    disease = db.execute(text(f"""
        SELECT
            COUNT(*) AS disease_records,
            COUNT(DISTINCT d.epidemiology_unit_id) AS affected_units,
            COALESCE(SUM(d.infected_count), 0) AS infected_count,
            COALESCE(SUM(d.dead_count), 0) AS dead_count
        FROM gis_disease_occurrences d
        {disease_clause}
    """), disease_params).mappings().one()

    return {
        "vaccinated_units": int(vaccination["vaccinated_units"] or 0),
        "vaccinated_animals": int(vaccination["vaccinated_animals"] or 0),
        "adverse_events": int(vaccination["adverse_events"] or 0),
        "disease_records": int(disease["disease_records"] or 0),
        "affected_units": int(disease["affected_units"] or 0),
        "infected_count": int(disease["infected_count"] or 0),
        "dead_count": int(disease["dead_count"] or 0),
        "interpretation": (
            "رخداد بیماری پس از واکسیناسیون صرفاً یک سیگنال برای بررسی است "
            "و به‌تنهایی اثبات‌کننده عدم اثربخشی واکسن نیست."
        ),
    }


def unit_detail(db: Session, unit_code: str) -> dict[str, Any]:
    return {
        "unit_code": unit_code,
        "vaccination": units(db, unit_code=unit_code),
        "vaccines": vaccines(db),
        "effectiveness": effectiveness(db),
    }
'@

# ============================================================
# 2) API endpoint
# ============================================================
Write-Utf8NoBom "$Root\app\api\v1\endpoints\gis\vaccination_kpi.py" @'
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.gis.vaccination_kpi_service import (
    alerts,
    counties,
    dashboard,
    effectiveness,
    unit_detail,
    units,
    vaccines,
)

router = APIRouter(
    prefix="/gis/kpi/vaccination",
    tags=["GIS Vaccination KPI"],
)


@router.get("/dashboard")
def vaccination_dashboard(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return dashboard(db, province_code, county_code, vaccine_type)


@router.get("/counties")
def vaccination_counties(
    province_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return counties(db, province_code, vaccine_type)


@router.get("/vaccines")
def vaccination_vaccines(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return vaccines(db, province_code, county_code)


@router.get("/units")
def vaccination_units(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return units(db, province_code, county_code, vaccine_type)


@router.get("/alerts")
def vaccination_alerts(
    province_code: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return alerts(db, province_code)


@router.get("/effectiveness")
def vaccination_effectiveness(
    province_code: str | None = Query(None),
    county_code: str | None = Query(None),
    vaccine_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return effectiveness(db, province_code, county_code, vaccine_type)


@router.get("/unit/{unit_code}")
def vaccination_unit_detail(
    unit_code: str,
    db: Session = Depends(get_db),
):
    return unit_detail(db, unit_code)
'@

# ============================================================
# 3) Register router in app/api/v1/router.py
# ============================================================
$routerFile = "$Root\app\api\v1\router.py"
$routerText = [System.IO.File]::ReadAllText($routerFile, [System.Text.Encoding]::UTF8)

if ($routerText -notmatch "vaccination_kpi") {
    $needle = "from app.api.v1 import (`r`n    supervision,"
    $replacement = "from app.api.v1 import (`r`n    supervision,`r`n)`r`n`r`nfrom app.api.v1.endpoints.gis import vaccination_kpi"
    $routerText = $routerText.Replace($needle, $replacement)

    $needle2 = "    organization_geography.router,`r`n"
    if ($routerText -notmatch "vaccination_kpi\.router") {
        $routerText = $routerText.Replace(
            $needle2,
            $needle2 + "    vaccination_kpi.router,`r`n"
        )
    }
    Write-Utf8NoBom $routerFile $routerText
}

# ============================================================
# 4) Alembic migration: KPI materialization/alerts
# ============================================================
Write-Utf8NoBom "$Root\alembic\versions\add_vaccination_kpi_tables.py" @'
"""add vaccination KPI snapshot and alert tables

Revision ID: add_vaccination_kpi_tables
Revises:
Create Date: 2026-08-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "add_vaccination_kpi_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "gis_vaccination_kpi_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("snapshot_date", sa.Date(), nullable=False, index=True),
        sa.Column("province_code", sa.String(length=50), nullable=True, index=True),
        sa.Column("county_code", sa.String(length=50), nullable=True, index=True),
        sa.Column("unit_code", sa.String(length=100), nullable=True, index=True),
        sa.Column("vaccine_type", sa.String(length=255), nullable=True, index=True),
        sa.Column("coverage_percent", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("eligible_animals", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("vaccinated_animals", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("remaining_animals", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("adverse_events", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("adverse_event_rate_percent", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("effectiveness_signal", sa.String(length=50), nullable=True),
        sa.Column("metrics", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "gis_vaccination_kpi_alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("snapshot_date", sa.Date(), nullable=False, index=True),
        sa.Column("severity", sa.String(length=30), nullable=False, index=True),
        sa.Column("alert_type", sa.String(length=80), nullable=False, index=True),
        sa.Column("province_code", sa.String(length=50), nullable=True, index=True),
        sa.Column("county_code", sa.String(length=50), nullable=True, index=True),
        sa.Column("unit_code", sa.String(length=100), nullable=True, index=True),
        sa.Column("vaccine_type", sa.String(length=255), nullable=True, index=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", postgresql.JSONB(), nullable=True),
        sa.Column("is_resolved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table("gis_vaccination_kpi_alerts")
    op.drop_table("gis_vaccination_kpi_snapshots")
'@

# ============================================================
# 5) Checks
# ============================================================
$files = @(
    "$Root\app\services\gis\vaccination_kpi_service.py",
    "$Root\app\api\v1\endpoints\gis\vaccination_kpi.py",
    "$Root\app\api\v1\router.py",
    "$Root\alembic\versions\add_vaccination_kpi_tables.py"
)

foreach ($f in $files) {
    if (!(Test-Path $f)) { throw "Missing generated file: $f" }
}

& "$Root\.venv\Scripts\python.exe" -m compileall `
    "$Root\app\services\gis\vaccination_kpi_service.py" `
    "$Root\app\api\v1\endpoints\gis\vaccination_kpi.py" `
    "$Root\app\api\v1\router.py" `
    "$Root\alembic\versions\add_vaccination_kpi_tables.py"

if ($LASTEXITCODE -ne 0) { throw "compileall failed" }

& "$Root\.venv\Scripts\python.exe" -c "from app.services.gis.vaccination_kpi_service import dashboard, counties, vaccines, units, alerts, effectiveness; from app.api.v1.endpoints.gis.vaccination_kpi import router; from app.api.v1.router import api_router; print('KPI IMPORT CHECK: OK')"

if ($LASTEXITCODE -ne 0) { throw "import check failed" }

# Migration is intentionally not auto-run here because the existing Alembic
# graph must be verified before applying a migration with an empty down_revision.
Write-Host ""
Write-Host "VACCINATION KPI MODULE CREATED"
Write-Host "Compile/import checks completed."
Write-Host "Review Alembic head before running upgrade."
