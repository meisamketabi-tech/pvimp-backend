from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Iterable

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.gis.vaccination_kpi_service import (
    ANIMAL_GROUP_LABELS,
    _coverage_status,
    _filters,
    _metric_cte,
    _pct,
)

DEFAULT_NEAR_EXPIRY_DAYS = 90
BOOSTER_ALERT_DAYS = 21
FMD_IMMUNITY_DAYS = 182
DEFAULT_IMMUNITY_DAYS = 365

EXECUTIVE_VACCINES = (
    "شاربن", "تب برفکی", "آبله", "لمپی‌اسکین", "PPR",
    "FD REV1", "بروسلوز میش", "RD IRIBA", "FD IRIBA", "هاری",
)


def _apply_scope(where: str, params: dict[str, Any], allowed_county_codes: set[str] | None):
    if allowed_county_codes is None:
        return where, params
    if not allowed_county_codes:
        return f"{where} AND 1=0", params
    if "county_code" not in params:
        where += " AND v.county_code = ANY(:allowed_county_codes)"
        params = {**params, "allowed_county_codes": list(sorted(allowed_county_codes))}
    return where, params


def _metric_rows(db: Session, province_code: str | None, county_code: str | None, allowed_county_codes: set[str] | None):
    where, params = _filters(province_code, county_code, None, None)
    where, params = _apply_scope(where, params, allowed_county_codes)
    rows = db.execute(text(f"""
        {_metric_cte(where)}
        SELECT unit_code, MAX(unit_name) unit_name,
               MAX(province_code) province_code, MAX(province_name) province_name,
               MAX(county_code) county_code, MAX(county_name) county_name,
               vaccine_type, MAX(disease_name) disease_name, animal_group,
               MAX(vaccine_brand) vaccine_brand,
               SUM(records) records,
               SUM(recorded_total_animals) recorded_total_animals,
               SUM(target_population) target_population,
               SUM(vaccinated_animals) vaccinated_animals,
               SUM(adverse_events) adverse_events,
               MAX(last_vaccination_date) last_vaccination_date
        FROM with_target
        GROUP BY unit_code, vaccine_type, animal_group
        ORDER BY county_name NULLS LAST, unit_name NULLS LAST, vaccine_type NULLS LAST
    """), params).mappings().all()
    return [dict(r) for r in rows]


def _metric(row: dict[str, Any]) -> dict[str, Any]:
    target = int(row.get("target_population") or 0)
    vaccinated = int(row.get("vaccinated_animals") or 0)
    coverage = _pct(vaccinated, target)
    return {
        "unit_code": row.get("unit_code"), "unit_name": row.get("unit_name"),
        "province_code": row.get("province_code"), "province_name": row.get("province_name"),
        "county_code": row.get("county_code"), "county_name": row.get("county_name"),
        "vaccine_type": row.get("vaccine_type"), "disease_name": row.get("disease_name"),
        "animal_group": row.get("animal_group"),
        "animal_group_name": ANIMAL_GROUP_LABELS.get(row.get("animal_group"), row.get("animal_group")),
        "vaccine_brand": row.get("vaccine_brand"), "records": int(row.get("records") or 0),
        "recorded_total_animals": int(row.get("recorded_total_animals") or 0),
        "target_population": target, "vaccinated_animals": vaccinated,
        "remaining_animals": max(target - vaccinated, 0), "coverage_percent": coverage,
        "progress_percent": coverage, "status": _coverage_status(coverage, target),
        "adverse_events": int(row.get("adverse_events") or 0),
        "last_vaccination_date": row.get("last_vaccination_date"),
    }


def _aggregate(rows: Iterable[dict[str, Any]]):
    vaccine_groups: dict[tuple[str, str], dict[str, Any]] = {}
    counties: dict[str, dict[str, Any]] = {}
    units: list[dict[str, Any]] = []
    provinces: set[str] = set()
    for raw in rows:
        row = _metric(raw)
        units.append(row)
        if row.get("province_name"):
            provinces.add(str(row["province_name"]))
        key = (str(row.get("vaccine_type") or ""), str(row.get("animal_group") or ""))
        v = vaccine_groups.setdefault(key, {
            "vaccine_type": row.get("vaccine_type"), "disease_name": row.get("disease_name"),
            "animal_group": row.get("animal_group"), "animal_group_name": row.get("animal_group_name"),
            "vaccine_brand": row.get("vaccine_brand"), "units": set(), "counties": set(),
            "records": 0, "target_population": 0, "vaccinated_animals": 0,
            "remaining_animals": 0, "adverse_events": 0, "last_vaccination_date": None,
        })
        v["units"].add(str(row.get("unit_code") or ""))
        if row.get("county_code") is not None:
            v["counties"].add(str(row["county_code"]))
        for key2 in ("records", "target_population", "vaccinated_animals", "remaining_animals", "adverse_events"):
            v[key2] += row[key2]
        if row.get("last_vaccination_date") and (v["last_vaccination_date"] is None or row["last_vaccination_date"] > v["last_vaccination_date"]):
            v["last_vaccination_date"] = row["last_vaccination_date"]
        ckey = str(row.get("county_code") or "")
        c = counties.setdefault(ckey, {"county_code": row.get("county_code"), "county_name": row.get("county_name"), "units": set(), "target_population": 0, "vaccinated_animals": 0, "remaining_animals": 0})
        c["units"].add(str(row.get("unit_code") or ""))
        c["target_population"] += row["target_population"]
        c["vaccinated_animals"] += row["vaccinated_animals"]
        c["remaining_animals"] += row["remaining_animals"]

    vaccines = []
    for v in vaccine_groups.values():
        target, vaccinated = int(v["target_population"]), int(v["vaccinated_animals"])
        vaccines.append({**v, "units": len(v["units"]), "counties": len(v["counties"]),
            "target_population": target, "vaccinated_animals": vaccinated,
            "remaining_animals": int(v["remaining_animals"]), "coverage_percent": _pct(vaccinated, target),
            "progress_percent": _pct(vaccinated, target), "status": _coverage_status(_pct(vaccinated, target), target),
            "adverse_event_rate_percent": _pct(v["adverse_events"], vaccinated)})
    county_rows = []
    for c in counties.values():
        target, vaccinated = int(c["target_population"]), int(c["vaccinated_animals"])
        coverage = _pct(vaccinated, target)
        county_rows.append({**c, "units": len(c["units"]), "target_population": target,
            "vaccinated_animals": vaccinated, "remaining_animals": int(c["remaining_animals"]),
            "coverage_percent": coverage, "progress_percent": coverage, "status": _coverage_status(coverage, target)})
    total_target = sum(x["target_population"] for x in units)
    total_vaccinated = sum(x["vaccinated_animals"] for x in units)
    summary = {
        "units": len({str(x.get("unit_code")) for x in units if x.get("unit_code")}),
        "counties": len({str(x.get("county_code")) for x in units if x.get("county_code")}),
        "vaccine_types": len({str(x.get("vaccine_type")) for x in units if x.get("vaccine_type")}),
        "target_population": total_target, "vaccinated_animals": total_vaccinated,
        "remaining_animals": max(total_target - total_vaccinated, 0),
        "coverage_percent": _pct(total_vaccinated, total_target), "coverage_is_valid": False,
        "coverage_note": "پوشش کل بین واکسن‌های مختلف جمع‌پذیر نیست؛ KPI معتبر در سطح واکسن و گروه دام نمایش داده می‌شود.",
        "province_names": sorted(provinces),
    }
    return vaccines, county_rows, summary, units


def _booster_alerts(units: list[dict[str, Any]], today: date | None = None):
    today = today or date.today()
    cutoff = today + timedelta(days=BOOSTER_ALERT_DAYS)
    alerts = []
    for row in units:
        last = row.get("last_vaccination_date")
        if not last:
            continue
        immunity_days = FMD_IMMUNITY_DAYS if "تب برفکی" in str(row.get("vaccine_type") or "") else DEFAULT_IMMUNITY_DAYS
        due = last + timedelta(days=immunity_days)
        if due <= cutoff:
            alerts.append({
                "severity": "OVERDUE" if due < today else "DUE_SOON",
                "county_code": row.get("county_code"), "county_name": row.get("county_name"),
                "unit_code": row.get("unit_code"), "unit_name": row.get("unit_name"),
                "vaccine_type": row.get("vaccine_type"), "animal_group": row.get("animal_group"),
                "animal_group_name": row.get("animal_group_name"), "last_vaccination_date": last,
                "due_date": due, "days_until_due": (due - today).days, "immunity_days": immunity_days,
            })
    alerts.sort(key=lambda x: (x["due_date"], str(x.get("county_name") or ""), str(x.get("unit_name") or "")))
    by_county: dict[str, dict[str, Any]] = {}
    for item in alerts:
        key = str(item.get("county_code") or "")
        b = by_county.setdefault(key, {"county_code": item.get("county_code"), "county_name": item.get("county_name"), "due_soon": 0, "overdue": 0, "units": []})
        b["overdue" if item["severity"] == "OVERDUE" else "due_soon"] += 1
        b["units"].append(item)
    county_alerts = [{**x, "total_alerts": x["due_soon"] + x["overdue"]} for x in by_county.values()]
    county_alerts.sort(key=lambda x: (-x["overdue"], -x["due_soon"], str(x.get("county_name") or "")))
    return alerts, county_alerts


def _inventory(db: Session, county_code: str | None, allowed_county_codes: set[str] | None, near_expiry_days: int):
    clauses = ["1=1"]
    params: dict[str, Any] = {"near_expiry_days": max(1, min(int(near_expiry_days), 365))}
    if county_code:
        clauses.append("county_name = :county_code")
        params["county_code"] = county_code
    elif allowed_county_codes is not None:
        if not allowed_county_codes:
            clauses.append("1=0")
        else:
            clauses.append("county_name = ANY(:allowed_county_codes)")
            params["allowed_county_codes"] = list(sorted(allowed_county_codes))
    rows = db.execute(text(f"""
        SELECT vaccine_type, vaccine_brand, manufacturer, batch_number, province_name, county_name,
               epidemiology_unit_code, epidemiology_unit_name, COALESCE(package_count,0) package_count, expiration_date
        FROM gis_vaccine_inventories WHERE {' AND '.join(clauses)}
        ORDER BY expiration_date NULLS LAST, vaccine_type NULLS LAST
    """), params).mappings().all()
    today, cutoff = date.today(), date.today() + timedelta(days=params["near_expiry_days"])
    inventory, near = [], []
    for r in rows:
        item = {"vaccine_type": r["vaccine_type"], "vaccine_brand": r["vaccine_brand"], "manufacturer": r["manufacturer"],
            "batch_number": r["batch_number"], "province_name": r["province_name"], "county_name": r["county_name"],
            "unit_code": r["epidemiology_unit_code"], "unit_name": r["epidemiology_unit_name"],
            "package_count": int(r["package_count"] or 0), "expiration_date": r["expiration_date"],
            "days_to_expiry": (r["expiration_date"] - today).days if r["expiration_date"] else None}
        inventory.append(item)
        if r["expiration_date"] and r["expiration_date"] <= cutoff:
            near.append(item)
    return {"total_lots": len(inventory), "total_packages": sum(x["package_count"] for x in inventory),
        "near_expiry_days": params["near_expiry_days"], "near_expiry_lots": len(near), "near_expiry": near[:100], "inventory": inventory[:300]}


def _surveillance(db: Session, province_code: str | None, county_code: str | None, allowed_county_codes: set[str] | None):
    clauses, params = ["1=1"], {}
    if province_code:
        clauses.append("province_code = :province_code"); params["province_code"] = province_code
    if county_code:
        clauses.append("county_code = :county_code"); params["county_code"] = county_code
    elif allowed_county_codes is not None:
        if not allowed_county_codes:
            clauses.append("1=0")
        else:
            clauses.append("county_code = ANY(:allowed_county_codes)"); params["allowed_county_codes"] = list(sorted(allowed_county_codes))
    rows = db.execute(text(f"""
        SELECT care_type, COALESCE(SUM(total_animals),0) total_animals,
               COALESCE(SUM(positive_count),0) positive_count, COALESCE(SUM(negative_count),0) negative_count,
               COALESCE(SUM(suspicious_count),0) suspicious_count, COUNT(*) records
        FROM gis_enable_cares WHERE {' AND '.join(clauses)} GROUP BY care_type ORDER BY care_type
    """), params).mappings().all()
    definitions = [
        ("خونگیری (تست بروسلوز)", ("بروسلوز", "خونگیری")),
        ("تست سل", ("سل",)),
        ("تست مشمشه — سرمی و مالئیناسیون", ("مشمشه", "مالئین")),
    ]
    result = []
    for label, needles in definitions:
        match = [r for r in rows if any(n in str(r["care_type"] or "") for n in needles)]
        result.append({"label": label, "records": sum(int(r["records"] or 0) for r in match),
            "total_animals": sum(int(r["total_animals"] or 0) for r in match),
            "positive_count": sum(int(r["positive_count"] or 0) for r in match),
            "negative_count": sum(int(r["negative_count"] or 0) for r in match),
            "suspicious_count": sum(int(r["suspicious_count"] or 0) for r in match)})
    return result


def overview(db: Session, province_code: str | None = None, county_code: str | None = None,
             allowed_county_codes: set[str] | None = None, near_expiry_days: int = DEFAULT_NEAR_EXPIRY_DAYS):
    raw = _metric_rows(db, province_code, county_code, allowed_county_codes)
    vaccines, counties, summary, units = _aggregate(raw)
    booster_alerts, booster_by_county = _booster_alerts(units)
    return {
        "summary": summary, "executive_vaccines": list(EXECUTIVE_VACCINES), "vaccines": vaccines,
        "counties": counties, "booster_alerts": booster_alerts[:300], "booster_by_county": booster_by_county,
        "booster_alert_days": BOOSTER_ALERT_DAYS, "fmd_immunity_days": FMD_IMMUNITY_DAYS,
        "default_immunity_days": DEFAULT_IMMUNITY_DAYS,
        "inventory_summary": _inventory(db, county_code, allowed_county_codes, near_expiry_days),
        "surveillance": _surveillance(db, province_code, county_code, allowed_county_codes),
        "generated_at": date.today().isoformat(),
    }
