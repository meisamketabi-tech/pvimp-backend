from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.gis.vaccination_kpi_service import ANIMAL_GROUP_LABELS, _filters, _pct, _coverage_status, _target_expr
from app.services.gis.vaccination_overview_service import (
    BOOSTER_ALERT_DAYS,
    DEFAULT_IMMUNITY_DAYS,
    DEFAULT_NEAR_EXPIRY_DAYS,
    EXECUTIVE_VACCINES,
    FMD_IMMUNITY_DAYS,
    _aggregate,
    _apply_scope,
    _booster_alerts,
    _inventory,
    _surveillance,
)


def _metric_rows_fast(
    db: Session,
    province_code: str | None,
    county_code: str | None,
    allowed_county_codes: set[str] | None,
) -> list[dict[str, Any]]:
    where, params = _filters(province_code, county_code, None, None)
    where, params = _apply_scope(where, params, allowed_county_codes)

    # The optimized PostgreSQL view is fast when read once, but wrapping it in
    # the large window/grouping CTE caused PostgreSQL to repeatedly expand the
    # view and pushed the API metric query above 17 seconds. Materialize only
    # the columns needed by the KPI calculation once per request, then aggregate
    # the small temp relation.
    db.execute(text("DROP TABLE IF EXISTS pg_temp.vaccination_metric_source"))
    db.execute(text(f"""
        CREATE TEMP TABLE vaccination_metric_source ON COMMIT DROP AS
        SELECT
            v.epidemiology_unit_code,
            v.epidemiology_unit_name,
            v.province_code,
            v.province_name,
            v.county_code,
            v.county_name,
            v.vaccine_type,
            v.disease_name,
            v.animal_group,
            v.vaccine_brand,
            v.is_composite_animal,
            v.total_animals,
            v.vaccinated_animals,
            v.shock_count,
            v.death_count,
            v.abortion_count,
            v.hypersensitivity_count,
            v.local_complication_count,
            v.vaccination_date
        FROM gis_vaccination_kpi v
        WHERE {where}
    """), params)
    db.execute(text("ANALYZE vaccination_metric_source"))

    rows = db.execute(text(f"""
        WITH scoped AS (
            SELECT v.*,
                   MAX(CASE WHEN v.is_composite_animal = TRUE THEN 1 ELSE 0 END)
                     OVER (
                         PARTITION BY v.epidemiology_unit_code, v.vaccine_type, v.animal_group
                     ) AS has_composite
            FROM vaccination_metric_source v
        ), deduped AS (
            SELECT s.*
            FROM scoped s
            WHERE s.is_composite_animal = TRUE OR s.has_composite = 0
        ), unit_metrics AS (
            SELECT
                d.epidemiology_unit_code AS unit_code,
                MAX(d.epidemiology_unit_name) AS unit_name,
                MAX(d.province_code) AS province_code,
                MAX(d.province_name) AS province_name,
                MAX(d.county_code) AS county_code,
                MAX(d.county_name) AS county_name,
                d.vaccine_type,
                MAX(d.disease_name) AS disease_name,
                d.animal_group,
                MAX(d.vaccine_brand) AS vaccine_brand,
                COUNT(*) AS records,
                COALESCE(SUM(d.total_animals), 0) AS recorded_total_animals,
                COALESCE(SUM(d.vaccinated_animals), 0) AS vaccinated_animals,
                COALESCE(SUM(d.shock_count), 0)
                  + COALESCE(SUM(d.death_count), 0)
                  + COALESCE(SUM(d.abortion_count), 0)
                  + COALESCE(SUM(d.hypersensitivity_count), 0)
                  + COALESCE(SUM(d.local_complication_count), 0) AS adverse_events,
                MAX(d.vaccination_date) AS last_vaccination_date
            FROM deduped d
            GROUP BY d.epidemiology_unit_code, d.vaccine_type, d.animal_group
        ), with_target AS (
            SELECT m.*, COALESCE(({_target_expr()}), 0) AS target_population
            FROM unit_metrics m
            LEFT JOIN gis_epidemiology_units u ON u.unit_code = m.unit_code
        )
        SELECT
            unit_code,
            MAX(unit_name) AS unit_name,
            MAX(province_code) AS province_code,
            MAX(province_name) AS province_name,
            MAX(county_code) AS county_code,
            MAX(county_name) AS county_name,
            vaccine_type,
            MAX(disease_name) AS disease_name,
            animal_group,
            MAX(vaccine_brand) AS vaccine_brand,
            SUM(records) AS records,
            SUM(recorded_total_animals) AS recorded_total_animals,
            SUM(target_population) AS target_population,
            SUM(vaccinated_animals) AS vaccinated_animals,
            SUM(adverse_events) AS adverse_events,
            MAX(last_vaccination_date) AS last_vaccination_date
        FROM with_target
        GROUP BY unit_code, vaccine_type, animal_group
        ORDER BY county_name NULLS LAST, unit_name NULLS LAST, vaccine_type NULLS LAST
    """)).mappings().all()
    return [dict(r) for r in rows]


def overview(
    db: Session,
    province_code: str | None = None,
    county_code: str | None = None,
    allowed_county_codes: set[str] | None = None,
    near_expiry_days: int = DEFAULT_NEAR_EXPIRY_DAYS,
):
    raw = _metric_rows_fast(db, province_code, county_code, allowed_county_codes)
    vaccines, counties, summary, units = _aggregate(raw)
    booster_alerts, booster_by_county = _booster_alerts(units)
    return {
        "summary": summary,
        "executive_vaccines": list(EXECUTIVE_VACCINES),
        "vaccines": vaccines,
        "counties": counties,
        "booster_alerts": booster_alerts[:300],
        "booster_by_county": booster_by_county,
        "booster_alert_days": BOOSTER_ALERT_DAYS,
        "fmd_immunity_days": FMD_IMMUNITY_DAYS,
        "default_immunity_days": DEFAULT_IMMUNITY_DAYS,
        "inventory_summary": _inventory(db, county_code, allowed_county_codes, near_expiry_days),
        "surveillance": _surveillance(db, province_code, county_code, allowed_county_codes),
        "generated_at": date.today().isoformat(),
    }
