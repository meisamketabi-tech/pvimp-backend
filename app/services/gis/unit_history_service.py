from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


def unit_history(
    db: Session,
    unit_code: str,
) -> dict[str, Any]:
    unit_code = str(unit_code).strip()

    if not unit_code:
        return {
            "unit_code": unit_code,
            "unit_name": None,
            "history": [],
        }

    unit = db.execute(
        text(
            """
            SELECT
                id,
                unit_code,
                unit_name,
                province_id,
                county_id
            FROM gis_epidemiology_units
            WHERE unit_code = :unit_code
            LIMIT 1
            """
        ),
        {"unit_code": unit_code},
    ).mappings().first()

    if not unit:
        return {
            "unit_code": unit_code,
            "unit_name": None,
            "history": [],
        }

    vaccination_rows = db.execute(
        text(
            """
            SELECT
                vaccination_date AS operation_date,
                'VACCINATION' AS operation_type,
                vaccine_type AS title,
                vaccine_brand AS detail,
                vaccinated_animals AS animal_count,
                animal_type,
                operation_type AS subtype
            FROM gis_vaccination_performances
            WHERE epidemiology_unit_code = :unit_code
            """
        ),
        {"unit_code": unit_code},
    ).mappings().all()

    spraying_rows = db.execute(
        text(
            """
            SELECT
                spraying_date AS operation_date,
                'SPRAYING' AS operation_type,
                poison_type AS title,
                plan_type AS detail,
                sprayed_animal_count AS animal_count,
                animal_type,
                operation_type AS subtype
            FROM gis_spraying
            WHERE epidemiology_unit_code = :unit_code
            """
        ),
        {"unit_code": unit_code},
    ).mappings().all()

    history: list[dict[str, Any]] = []

    for row in vaccination_rows:
        history.append(
            {
                "date": row["operation_date"],
                "operation": "واکسیناسیون",
                "operation_code": "VACCINATION",
                "title": row["title"],
                "detail": row["detail"],
                "animal_count": row["animal_count"] or 0,
                "animal_type": row["animal_type"],
                "subtype": row["subtype"],
            }
        )

    for row in spraying_rows:
        history.append(
            {
                "date": row["operation_date"],
                "operation": "سمپاشی",
                "operation_code": "SPRAYING",
                "title": row["title"],
                "detail": row["detail"],
                "animal_count": row["animal_count"] or 0,
                "animal_type": row["animal_type"],
                "subtype": row["subtype"],
            }
        )

    history.sort(
        key=lambda item: (
            item["date"] is not None,
            item["date"],
        ),
        reverse=True,
    )

    return {
        "unit_code": unit["unit_code"],
        "unit_name": unit["unit_name"],
        "history": history,
    }