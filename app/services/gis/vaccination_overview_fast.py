from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.gis.vaccination_kpi_service import _filters, _target_expr
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

_MV_NAME = "gis_vaccination_kpi_mv"
_REFRESH_LOCK_KEY = 782341


def _ensure_kpi_cache_fresh(db: Session) -> None:
    """Refresh the materialized KPI cache only when source rows changed.

    The vaccination importer is append-only, so comparing COUNT/MAX(id) is a
    cheap freshness check. The advisory transaction lock prevents concurrent
    requests from refreshing the cache more than once after an import.
    """
    source = db.execute(
        text(
            """
            SELECT COUNT(*) AS row_count, COALESCE(MAX(id), 0) AS max_id
            FROM gis_vaccination_performances
            """
        )
    ).mappings().one()

    cached = db.execute(
        text(
            f"""
            SELECT COUNT(*) AS row_count, COALESCE(MAX(id), 0) AS max_id
            FROM {_MV_NAME}
            """
        )
    ).mappings().one()

    if (
        int(source["row_count"]) == int(cached["row_count"])
        and int(source["max_id"]) == int(cached["max_id"])
    ):
        return

    db.execute(text("SELECT pg_advisory_xact_lock(:lock_key)"), {"lock_key": _REFRESH_LOCK_KEY})

    # Another request may have refreshed the cache while we waited.
    cached = db.execute(
        text(
            f"""
            SELECT COUNT(*) AS row_count, COALESCE(MAX(id), 0) AS max_id
            FROM {_MV_NAME}
            """
        )
    ).mappings().one()

    if (
        int(source["row_count"]) == int(cached["row_count"])
        and int(source["max_id"]) == int(cached["max_id"])
    ):
        return

    db.execute(text(f"REFRESH MATERIALIZED VIEW {_MV_NAME}"))
    db.execute(text(f"ANALYZE {_MV_NAME}"))


def _metric_rows_fast(
    db: Session,
    province_code: str | None,
    county_code: str | None,
    allowed_county_codes: set[str] | None,
) -> list[dict[str, Any]]:
    _ensure_kpi_cache_fresh(db)

    where, params = _filters(province_code, county_code, None, None)
    where, params = _apply_scope(where, params, allowed_county_codes)

    rows = db.execute(
        text(
            f"""
            WITH scoped AS MATERIALIZED (
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
                FROM {_MV_NAME} v
                WHERE {where}
            ), flagged AS MATERIALIZED (
                SELECT s.*,
                       MAX(CASE WHEN s.is_composite_animal = TRUE THEN 1 ELSE 0 END)
                         OVER (
                             PARTITION BY s.epidemiology_unit_code, s.vaccine_type, s.animal_group
                         ) AS has_composite
                FROM scoped s
            ), unit_metrics AS (
                SELECT
                    f.epidemiology_unit_code AS unit_code,
                    MAX(f.epidemiology_unit_name) AS unit_name,
                    MAX(f.province_code) AS province_code,
                    MAX(f.province_name) AS province_name,
                    MAX(f.county_code) AS county_code,
                    MAX(f.county_name) AS county_name,
                    f.vaccine_type,
                    MAX(f.disease_name) AS disease_name,
                    f.animal_group,
                    MAX(f.vaccine_brand) AS vaccine_brand,
                    COUNT(*) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0) AS records,
                    COALESCE(SUM(f.total_animals) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0), 0) AS recorded_total_animals,
                    COALESCE(SUM(f.vaccinated_animals) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0), 0) AS vaccinated_animals,
                    COALESCE(SUM(f.shock_count) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0), 0)
                      + COALESCE(SUM(f.death_count) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0), 0)
                      + COALESCE(SUM(f.abortion_count) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0), 0)
                      + COALESCE(SUM(f.hypersensitivity_count) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0), 0)
                      + COALESCE(SUM(f.local_complication_count) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0), 0) AS adverse_events,
                    MAX(f.vaccination_date) FILTER (WHERE f.is_composite_animal = TRUE OR f.has_composite = 0) AS last_vaccination_date
                FROM flagged f
                GROUP BY f.epidemiology_unit_code, f.vaccine_type, f.animal_group
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
            """
        ),
        params,
    ).mappings().all()
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
