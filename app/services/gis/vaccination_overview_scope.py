from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.gis.vaccination_overview_service import overview as _base_overview


def _scoped_inventory(db: Session, province_code: str | None, county_code: str | None, allowed_county_codes: set[str] | None, near_expiry_days: int) -> dict[str, Any]:
    clauses = ["1=1"]
    params: dict[str, Any] = {}
    if county_code:
        clauses.append("c.county_code = :county_code")
        params["county_code"] = county_code
    elif allowed_county_codes is not None:
        if not allowed_county_codes:
            clauses.append("1=0")
        else:
            clauses.append("c.county_code = ANY(:allowed_county_codes)")
            params["allowed_county_codes"] = list(sorted(allowed_county_codes))
    if province_code:
        clauses.append("p.province_code = :province_code")
        params["province_code"] = province_code

    rows = db.execute(text(f"""
        SELECT i.vaccine_type, i.vaccine_brand, i.manufacturer, i.batch_number,
               i.province_name, i.county_name, i.epidemiology_unit_code, i.epidemiology_unit_name,
               COALESCE(i.package_count,0) package_count, i.expiration_date
        FROM gis_vaccine_inventories i
        LEFT JOIN gis_counties c ON c.county_name = i.county_name
        LEFT JOIN gis_provinces p ON p.id = c.province_id
        WHERE {' AND '.join(clauses)}
        ORDER BY i.expiration_date NULLS LAST, i.vaccine_type NULLS LAST
    """), params).mappings().all()

    today = date.today()
    cutoff = today + timedelta(days=max(1, min(int(near_expiry_days), 365)))
    inventory, near = [], []
    for r in rows:
        item = {
            "vaccine_type": r["vaccine_type"], "vaccine_brand": r["vaccine_brand"], "manufacturer": r["manufacturer"],
            "batch_number": r["batch_number"], "province_name": r["province_name"], "county_name": r["county_name"],
            "unit_code": r["epidemiology_unit_code"], "unit_name": r["epidemiology_unit_name"],
            "package_count": int(r["package_count"] or 0), "expiration_date": r["expiration_date"],
            "days_to_expiry": (r["expiration_date"] - today).days if r["expiration_date"] else None,
        }
        inventory.append(item)
        if r["expiration_date"] and r["expiration_date"] <= cutoff:
            near.append(item)
    return {"total_lots": len(inventory), "total_packages": sum(x["package_count"] for x in inventory),
            "near_expiry_days": max(1, min(int(near_expiry_days), 365)), "near_expiry_lots": len(near),
            "near_expiry": near[:100], "inventory": inventory[:300]}


def overview(*, db: Session, province_code: str | None = None, county_code: str | None = None,
             allowed_county_codes: set[str] | None = None, near_expiry_days: int = 90):
    result = _base_overview(db=db, province_code=province_code, county_code=county_code,
                            allowed_county_codes=allowed_county_codes, near_expiry_days=near_expiry_days)
    result["inventory_summary"] = _scoped_inventory(db, province_code, county_code, allowed_county_codes, near_expiry_days)
    return result
