from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from app.services.gis.vaccination_classification import (
    classify_animal,
    classify_vaccine,
)


def normalize_vaccination_row(row: dict[str, Any]) -> dict[str, Any]:
    """Attach semantic KPI fields without modifying raw GIS values."""
    result = dict(row)

    vaccine = classify_vaccine(row.get("vaccine_type"))
    animal = classify_animal(row.get("animal_type"))

    result["raw_vaccine_type"] = vaccine.raw_name
    result["standard_vaccine_type"] = vaccine.standard_name
    result["standard_disease_name"] = vaccine.disease_name
    result["activity_type"] = vaccine.activity_type

    result.update(animal)
    return result


def normalize_vaccination_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_vaccination_row(row) for row in rows]


def is_kpi_row(row: dict[str, Any]) -> bool:
    return classify_vaccine(row.get("vaccine_type")).activity_type == "VACCINATION"
