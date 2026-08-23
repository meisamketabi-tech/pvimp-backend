from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

VACCINATION_VIEW = "gis_vaccination_kpi"

ANIMAL_GROUP_LABELS = {
    "LIGHT_LIVESTOCK": "دام سبک",
    "HEAVY_LIVESTOCK": "دام سنگین",
    "EQUINE": "تک‌سمی",
    "DOG": "سگ",
    "CAT": "گربه",
    "CAMEL": "شتر",
    "UNKNOWN": "نامشخص",
}


def _filters(province_code: str | None = None, county_code: str | None = None,
             vaccine_type: str | None = None, animal_group: str | None = None,
             unit_code: str | None = None) -> tuple[str, dict[str, Any]]:
    clauses = ["v.activity_type = 'VACCINATION'"]
    params: dict[str, Any] = {}
    if province_code:
        clauses.append("v.province_code = :province_code")
        params["province_code"] = province_code
    if county_code:
        clauses.append("v.county_code = :county_code")
        params["county_code"] = county_code
    if vaccine_type:
        clauses.append("v.vaccine_type = :vaccine_type")
        params["vaccine_type"] = vaccine_type
    if animal_group:
        clauses.append("v.animal_group = :animal_group")
        params["animal_group"] = animal_group
    if unit_code:
        clauses.append("v.epidemiology_unit_code = :unit_code")
        params["unit_code"] = unit_code
    return " AND ".join(clauses), params


def _pct(numerator: int | float | None, denominator: int | float | None) -> float:
    if not denominator:
        return 0.0
    return round(float(numerator or 0) * 100.0 / float(denominator), 2)


def _coverage_status(coverage: float, target: int) -> str:
    if target <= 0:
        return "NO_TARGET"
    if coverage <= 0:
        return "NO_COVERAGE"
    if coverage < 50:
        return "CRITICAL"
    if coverage < 75:
        return "WARNING"
    if coverage < 90:
        return "ON_TRACK"
    return "EXCELLENT"


def _target_expr(unit_alias: str = "u", metric_alias: str = "m") -> str:
    return f"""
        CASE {metric_alias}.animal_group
            WHEN 'LIGHT_LIVESTOCK' THEN
                COALESCE({unit_alias}.sheep_count, 0) + COALESCE({unit_alias}.goat_count, 0)
            WHEN 'HEAVY_LIVESTOCK' THEN
                COALESCE({unit_alias}.cattle_count, 0) + COALESCE({unit_alias}.buffalo_count, 0)
            WHEN 'EQUINE' THEN COALESCE({unit_alias}.horse_count, 0)
            WHEN 'DOG' THEN COALESCE({unit_alias}.dog_count, 0)
            WHEN 'CAMEL' THEN COALESCE({unit_alias}.camel_count, 0)
            ELSE 0
        END
    """


def _metric_cte(where: str) -> str:
    return f"""
        WITH scoped AS (
            SELECT v.*
            FROM {VACCINATION_VIEW} v
            WHERE {where}
        ),
        deduped AS (
            SELECT s.*
            FROM scoped s
            WHERE s.is_composite_animal = TRUE
               OR NOT EXISTS (
                    SELECT 1
                    FROM scoped c
                    WHERE c.epidemiology_unit_code = s.epidemiology_unit_code
                      AND c.vaccine_type = s.vaccine_type
                      AND c.animal_group = s.animal_group
                      AND c.is_composite_animal = TRUE
               )
        ),
        unit_metrics AS (
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
        ),
        with_target AS (
            SELECT
                m.*,
                COALESCE(({_target_expr("u", "m")}), 0) AS target_population
            FROM unit_metrics m
            LEFT JOIN gis_epidemiology_units u
              ON u.unit_code = m.unit_code
        )
    """


def _row_dict(row: Any) -> dict[str, Any]:
    target = int(row["target_population"] or 0)
    vaccinated = int(row["vaccinated_animals"] or 0)
    coverage = _pct(vaccinated, target)
    return {
        "unit_code": row["unit_code"],
        "unit_name": row["unit_name"],
        "province_code": row["province_code"],
        "province_name": row["province_name"],
        "county_code": row["county_code"],
        "county_name": row["county_name"],
        "vaccine_type": row["vaccine_type"],
        "disease_name": row["disease_name"],
        "animal_group": row["animal_group"],
        "animal_group_name": ANIMAL_GROUP_LABELS.get(row["animal_group"], row["animal_group"]),
        "vaccine_brand": row["vaccine_brand"],
        "records": int(row["records"] or 0),
        "recorded_total_animals": int(row["recorded_total_animals"] or 0),
        "target_population": target,
        "vaccinated_animals": vaccinated,
        "remaining_animals": max(target - vaccinated, 0),
        "coverage_percent": coverage,
        "status": _coverage_status(coverage, target),
        "adverse_events": int(row["adverse_events"] or 0),
        "adverse_event_rate_percent": _pct(row["adverse_events"], vaccinated),
        "last_vaccination_date": row["last_vaccination_date"],
        "target_source": "EPIDEMIOLOGY_UNIT_POPULATION" if target > 0 else "NO_TARGET",
    }


def dashboard(db: Session, province_code: str | None = None, county_code: str | None = None,
              vaccine_type: str | None = None, animal_group: str | None = None) -> dict[str, Any]:
    where, params = _filters(province_code, county_code, vaccine_type, animal_group)
    row = db.execute(text(f"""
        {_metric_cte(where)}
        SELECT COUNT(*) AS unit_vaccine_groups,
               COUNT(DISTINCT unit_code) AS units,
               COUNT(DISTINCT county_code) AS counties,
               COUNT(DISTINCT vaccine_type) AS vaccine_types,
               COALESCE(SUM(recorded_total_animals), 0) AS recorded_total_animals,
               COALESCE(SUM(target_population), 0) AS target_population,
               COALESCE(SUM(vaccinated_animals), 0) AS vaccinated_animals,
               COALESCE(SUM(adverse_events), 0) AS adverse_events,
               MAX(last_vaccination_date) AS last_vaccination_date
        FROM with_target
    """), params).mappings().one()
    target = int(row["target_population"] or 0)
    vaccinated = int(row["vaccinated_animals"] or 0)
    coverage = _pct(vaccinated, target)
    return {
        "unit_vaccine_groups": int(row["unit_vaccine_groups"] or 0),
        "units": int(row["units"] or 0),
        "counties": int(row["counties"] or 0),
        "vaccine_types": int(row["vaccine_types"] or 0),
        "recorded_total_animals": int(row["recorded_total_animals"] or 0),
        "target_population": target,
        "vaccinated_animals": vaccinated,
        "remaining_animals": max(target - vaccinated, 0),
        "coverage_percent": coverage,
        "coverage_status": _coverage_status(coverage, target),
        "adverse_events": int(row["adverse_events"] or 0),
        "adverse_event_rate_percent": _pct(row["adverse_events"], vaccinated),
        "last_vaccination_date": row["last_vaccination_date"],
        "coverage_is_valid": bool(vaccine_type or animal_group),
        "coverage_note": None if (vaccine_type or animal_group) else "پوشش واکسیناسیون بین واکسن‌های مختلف قابل تجمیع نیست؛ برای KPI پوشش باید واکسن و/یا گروه دام انتخاب شود.",
    }


def vaccines(db: Session, province_code: str | None = None, county_code: str | None = None,
             vaccine_type: str | None = None, animal_group: str | None = None,
             unit_code: str | None = None) -> list[dict[str, Any]]:
    where, params = _filters(province_code, county_code, vaccine_type, animal_group, unit_code)
    rows = db.execute(text(f"""
        {_metric_cte(where)}
        SELECT vaccine_type, MAX(disease_name) AS disease_name, animal_group,
               MAX(vaccine_brand) AS vaccine_brand,
               COUNT(DISTINCT unit_code) AS units,
               COUNT(DISTINCT county_code) AS counties,
               SUM(records) AS records,
               SUM(recorded_total_animals) AS recorded_total_animals,
               SUM(target_population) AS target_population,
               SUM(vaccinated_animals) AS vaccinated_animals,
               SUM(adverse_events) AS adverse_events,
               MAX(last_vaccination_date) AS last_vaccination_date
        FROM with_target
        GROUP BY vaccine_type, animal_group
        ORDER BY vaccine_type NULLS LAST, animal_group
    """), params).mappings().all()
    result = []
    for r in rows:
        target = int(r["target_population"] or 0)
        vaccinated = int(r["vaccinated_animals"] or 0)
        coverage = _pct(vaccinated, target)
        result.append({
            "vaccine_type": r["vaccine_type"],
            "disease_name": r["disease_name"],
            "animal_group": r["animal_group"],
            "animal_group_name": ANIMAL_GROUP_LABELS.get(r["animal_group"], r["animal_group"]),
            "vaccine_brand": r["vaccine_brand"],
            "units": int(r["units"] or 0),
            "counties": int(r["counties"] or 0),
            "records": int(r["records"] or 0),
            "recorded_total_animals": int(r["recorded_total_animals"] or 0),
            "target_population": target,
            "vaccinated_animals": vaccinated,
            "remaining_animals": max(target - vaccinated, 0),
            "coverage_percent": coverage,
            "status": _coverage_status(coverage, target),
            "adverse_events": int(r["adverse_events"] or 0),
            "adverse_event_rate_percent": _pct(r["adverse_events"], vaccinated),
            "last_vaccination_date": r["last_vaccination_date"],
            "target_source": "EPIDEMIOLOGY_UNIT_POPULATION" if target > 0 else "NO_TARGET",
        })
    return result


def counties(db: Session, province_code: str | None = None, vaccine_type: str | None = None,
             animal_group: str | None = None) -> list[dict[str, Any]]:
    where, params = _filters(province_code, None, vaccine_type, animal_group)
    rows = db.execute(text(f"""
        {_metric_cte(where)}
        SELECT county_code, MAX(county_name) AS county_name,
               COUNT(DISTINCT unit_code) AS units,
               SUM(records) AS records,
               SUM(target_population) AS target_population,
               SUM(recorded_total_animals) AS recorded_total_animals,
               SUM(vaccinated_animals) AS vaccinated_animals,
               SUM(adverse_events) AS adverse_events,
               MAX(last_vaccination_date) AS last_vaccination_date
        FROM with_target
        GROUP BY county_code
        ORDER BY county_name NULLS LAST
    """), params).mappings().all()
    result = []
    for r in rows:
        target = int(r["target_population"] or 0)
        vaccinated = int(r["vaccinated_animals"] or 0)
        coverage = _pct(vaccinated, target)
        result.append({
            "county_code": r["county_code"], "county_name": r["county_name"],
            "records": int(r["records"] or 0), "units": int(r["units"] or 0),
            "recorded_total_animals": int(r["recorded_total_animals"] or 0),
            "target_population": target, "vaccinated_animals": vaccinated,
            "remaining_animals": max(target - vaccinated, 0), "coverage_percent": coverage,
            "status": _coverage_status(coverage, target),
            "adverse_events": int(r["adverse_events"] or 0),
            "adverse_event_rate_percent": _pct(r["adverse_events"], vaccinated),
            "last_vaccination_date": r["last_vaccination_date"],
        })
    return result


def units(db: Session, province_code: str | None = None, county_code: str | None = None,
          vaccine_type: str | None = None, animal_group: str | None = None,
          unit_code: str | None = None) -> list[dict[str, Any]]:
    where, params = _filters(province_code, county_code, vaccine_type, animal_group, unit_code)
    rows = db.execute(text(f"""
        {_metric_cte(where)}
        SELECT unit_code, MAX(unit_name) AS unit_name,
               MAX(province_code) AS province_code, MAX(province_name) AS province_name,
               MAX(county_code) AS county_code, MAX(county_name) AS county_name,
               MAX(vaccine_type) AS vaccine_type, MAX(disease_name) AS disease_name,
               animal_group, MAX(vaccine_brand) AS vaccine_brand,
               SUM(records) AS records, SUM(recorded_total_animals) AS recorded_total_animals,
               SUM(target_population) AS target_population, SUM(vaccinated_animals) AS vaccinated_animals,
               SUM(adverse_events) AS adverse_events, MAX(last_vaccination_date) AS last_vaccination_date
        FROM with_target
        GROUP BY unit_code, animal_group
        ORDER BY county_name NULLS LAST, unit_name NULLS LAST
    """), params).mappings().all()
    return [_row_dict(row) for row in rows]


def vaccine_unit_report(db: Session, vaccine_type: str, province_code: str | None = None,
                        county_code: str | None = None, animal_group: str | None = None) -> list[dict[str, Any]]:
    return units(db, province_code, county_code, vaccine_type, animal_group)


def vaccine_unit_report_paginated(db: Session, vaccine_type: str, province_code: str | None = None,
                                  county_code: str | None = None, page: int = 1, page_size: int = 50,
                                  animal_group: str | None = None) -> dict[str, Any]:
    data = vaccine_unit_report(db, vaccine_type, province_code, county_code, animal_group)
    total = len(data)
    start = max(page - 1, 0) * page_size
    return {"page": page, "page_size": page_size, "total": total,
            "pages": (total + page_size - 1) // page_size if page_size else 0,
            "items": data[start:start + page_size]}


def vaccine_county_report(db: Session, vaccine_type: str, province_code: str | None = None,
                          animal_group: str | None = None) -> list[dict[str, Any]]:
    return counties(db, province_code, vaccine_type, animal_group)


def alerts(db: Session, province_code: str | None = None, vaccine_type: str | None = None,
           animal_group: str | None = None) -> list[dict[str, Any]]:
    result = []
    for row in counties(db, province_code, vaccine_type, animal_group):
        coverage = float(row["coverage_percent"] or 0)
        if row["target_population"] <= 0:
            result.append({"severity": "INFO", "type": "NO_TARGET", "county_code": row["county_code"], "county_name": row["county_name"], "message": "برای این شاخص جمعیت هدف ثبت نشده است.", "details": row})
        elif coverage < 50:
            result.append({"severity": "CRITICAL", "type": "LOW_COVERAGE", "county_code": row["county_code"], "county_name": row["county_name"], "message": "پوشش واکسیناسیون کمتر از ۵۰ درصد است.", "details": row})
        elif coverage < 75:
            result.append({"severity": "WARNING", "type": "LOW_COVERAGE", "county_code": row["county_code"], "county_name": row["county_name"], "message": "پوشش واکسیناسیون نیازمند پیگیری است.", "details": row})
    return result


def effectiveness(db: Session, province_code: str | None = None, county_code: str | None = None,
                  vaccine_type: str | None = None, animal_group: str | None = None,
                  unit_code: str | None = None) -> dict[str, Any]:
    where, params = _filters(province_code, county_code, vaccine_type, animal_group, unit_code)
    vaccination = db.execute(text(f"""
        {_metric_cte(where)}
        SELECT COUNT(DISTINCT unit_code) AS vaccinated_units,
               SUM(vaccinated_animals) AS vaccinated_animals,
               SUM(adverse_events) AS adverse_events,
               SUM(target_population) AS target_population
        FROM with_target
    """), params).mappings().one()

    disease_where = ["1=1"]
    disease_params: dict[str, Any] = {}
    if province_code:
        disease_where.append("d.province_code = :province_code")
        disease_params["province_code"] = province_code
    if county_code:
        disease_where.append("d.county_code = :county_code")
        disease_params["county_code"] = county_code
    if unit_code:
        disease_where.append("d.epidemiology_unit_code = :unit_code")
        disease_params["unit_code"] = unit_code
    if vaccine_type:
        disease_where.append("EXISTS (SELECT 1 FROM gis_vaccination_kpi vx WHERE vx.vaccine_type = :vaccine_type AND vx.disease_name = d.disease_name LIMIT 1)")
        disease_params["vaccine_type"] = vaccine_type
    disease = db.execute(text(f"""
        SELECT COUNT(*) AS disease_records,
               COUNT(DISTINCT d.epidemiology_unit_id) AS affected_units,
               COALESCE(SUM(d.infected_count),0) AS infected_count,
               COALESCE(SUM(d.dead_count),0) AS dead_count
        FROM gis_disease_occurrences d
        WHERE {' AND '.join(disease_where)}
    """), disease_params).mappings().one()

    vaccinated = int(vaccination["vaccinated_animals"] or 0)
    adverse = int(vaccination["adverse_events"] or 0)
    target = int(vaccination["target_population"] or 0)
    return {
        "vaccinated_units": int(vaccination["vaccinated_units"] or 0),
        "vaccinated_animals": vaccinated, "target_population": target,
        "coverage_percent": _pct(vaccinated, target),
        "adverse_events": adverse, "adverse_event_rate_percent": _pct(adverse, vaccinated),
        "disease_records": int(disease["disease_records"] or 0),
        "affected_units": int(disease["affected_units"] or 0),
        "infected_count": int(disease["infected_count"] or 0),
        "dead_count": int(disease["dead_count"] or 0),
        "interpretation": "رخداد بیماری پس از واکسیناسیون صرفاً سیگنال بررسی است و اثبات‌کننده علیت یا عدم اثربخشی واکسن نیست.",
    }


def unit_detail(db: Session, unit_code: str) -> dict[str, Any]:
    return {"unit_code": unit_code, "vaccination": units(db, unit_code=unit_code),
            "vaccines": vaccines(db, unit_code=unit_code), "effectiveness": effectiveness(db, unit_code=unit_code)}


def county_units_report(db: Session, county_id: int) -> dict[str, Any]:
    county = db.execute(text("SELECT county_code, county_name, province_code, province_name FROM gis_counties WHERE id = :id LIMIT 1"), {"id": county_id}).mappings().first()
    if not county:
        return {"county_id": county_id, "units_count": 0, "units": []}
    rows = units(db, county_code=str(county["county_code"]).strip())
    return {"county_id": county_id, "county_code": county["county_code"], "county_name": county["county_name"],
            "province_code": county["province_code"], "province_name": county["province_name"],
            "units_count": len(rows), "units": rows}


def vaccine_management_report(db: Session, province_code: str | None = None, county_code: str | None = None,
                              vaccine_type: str | None = None, animal_group: str | None = None) -> dict[str, Any]:
    return {"dashboard": dashboard(db, province_code, county_code, vaccine_type, animal_group),
            "counties": counties(db, province_code, vaccine_type, animal_group),
            "vaccines": vaccines(db, province_code, county_code, vaccine_type, animal_group),
            "units": units(db, province_code, county_code, vaccine_type, animal_group),
            "alerts": alerts(db, province_code, vaccine_type, animal_group)}
