from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


def _rows(db: Session, sql: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(row) for row in db.execute(text(sql), params).mappings().all()]


def unit_history(db: Session, unit_code: str) -> dict[str, Any]:
    unit_code = str(unit_code).strip()
    if not unit_code:
        return {"unit_code": unit_code, "unit_name": None, "history": [], "sections": {}}

    unit = db.execute(text("""
        SELECT u.id, u.unit_code, u.unit_name, u.latitude, u.longitude,
               u.sheep_count, u.goat_count, u.cattle_count, u.buffalo_count,
               u.horse_count, u.dog_count, u.camel_count, u.address,
               u.license_type, u.sanitary_license_number, u.operation_license_number,
               p.province_code, p.province_name, c.county_code, c.county_name
        FROM gis_epidemiology_units u
        LEFT JOIN gis_provinces p ON p.id = u.province_id
        LEFT JOIN gis_counties c ON c.id = u.county_id
        WHERE u.unit_code = :unit_code
        LIMIT 1
    """), {"unit_code": unit_code}).mappings().first()

    if not unit:
        return {"unit_code": unit_code, "unit_name": None, "history": [], "sections": {}}

    params = {"unit_code": unit_code}

    vaccination = _rows(db, """
        SELECT vaccination_date, vaccine_type, disease_name, animal_type, vaccine_brand,
               manufacturer, batch_number, operation_type, vaccination_center_name,
               total_animals, eligible_animals, vaccinated_animals, animal_count,
               rappel_vaccination, age_group, registration_date
        FROM gis_vaccination_performances
        WHERE epidemiology_unit_code = :unit_code
        ORDER BY vaccination_date DESC NULLS LAST, id DESC
    """, params)

    spraying = _rows(db, """
        SELECT spraying_date, plan_type, operation_type, poison_type, sprayed_area,
               sprayed_animal_count, animal_type, total_animals
        FROM gis_spraying
        WHERE epidemiology_unit_code = :unit_code
        ORDER BY spraying_date DESC NULLS LAST, id DESC
    """, params)

    surveillance = _rows(db, """
        SELECT enable_care_detail_vcode, enable_care_vcode, care_date, care_type,
               animal_type, age_group, total_animals, positive_count, negative_count,
               suspicious_count, epidemiology_unit_type, operation_license_type
        FROM gis_enable_cares
        WHERE epidemiology_unit_code = :unit_code
        ORDER BY care_date DESC NULLS LAST, id DESC
    """, params)

    samples = _rows(db, """
        SELECT send_sample_detail_vcode, send_sample_vcode, disease_name, animal_type,
               sample_type, sample_count, sampling_date, result_status
        FROM gis_send_sample_details
        WHERE epidemiology_unit_code = :unit_code
        ORDER BY sampling_date DESC NULLS LAST, id DESC
    """, params)

    lab_results = _rows(db, """
        SELECT send_sample_vcode, answer_no, answer_date, sampling_date, register_date,
               laboratory_code, laboratory_name, laboratory_type, laboratory_owner,
               sample_type, sample_count, animal_type, disease_name, result_status,
               isolate_name_1, isolate_name_2, serotype_a, serotype_o, serotype_asia1,
               unacceptable_cases
        FROM gis_laboratory_results
        WHERE epidemiology_unit_code = :unit_code
        ORDER BY answer_date DESC NULLS LAST, id DESC
    """, params)

    occurrences = _rows(db, """
        SELECT observation_detail_vcode, observation_vcode, disease_name, animal_type,
               start_date, report_date, registration_date, animal_count, exposed_count,
               infected_count, dead_count, slaughtered_count, total_animals,
               sample_taken, report_number, status, description
        FROM gis_disease_occurrences
        WHERE epidemiology_unit_code = :unit_code
        ORDER BY start_date DESC NULLS LAST, id DESC
    """, params)

    disease_reports = _rows(db, """
        SELECT observation_detail_vcode, observation_vcode, disease_name, animal_type,
               disease_start_date, total_animals, infected_count, death_count,
               slaughtered_count, destroyed_count, sampling, age_group,
               biting_animal, creator_user_name, source_unit_name
        FROM gis_disease_reports
        WHERE epidemiology_unit_code = :unit_code
        ORDER BY disease_start_date DESC NULLS LAST, id DESC
    """, params)

    history: list[dict[str, Any]] = []
    for row in vaccination:
        history.append({"date": row.get("vaccination_date"), "operation": "واکسیناسیون", "operation_code": "VACCINATION", "title": row.get("vaccine_type"), "detail": row.get("vaccine_brand"), "animal_count": row.get("vaccinated_animals") or 0, "animal_type": row.get("animal_type"), "subtype": row.get("operation_type")})
    for row in spraying:
        history.append({"date": row.get("spraying_date"), "operation": "سمپاشی", "operation_code": "SPRAYING", "title": row.get("poison_type"), "detail": row.get("plan_type"), "animal_count": row.get("sprayed_animal_count") or 0, "animal_type": row.get("animal_type"), "subtype": row.get("operation_type")})
    for row in surveillance:
        history.append({"date": row.get("care_date"), "operation": "پایش و مراقبت", "operation_code": "SURVEILLANCE", "title": row.get("care_type"), "detail": row.get("animal_type"), "animal_count": row.get("total_animals") or 0, "animal_type": row.get("animal_type"), "subtype": None})
    for row in samples:
        history.append({"date": row.get("sampling_date"), "operation": "ارسال نمونه", "operation_code": "SAMPLE", "title": row.get("disease_name"), "detail": row.get("sample_type"), "animal_count": row.get("sample_count") or 0, "animal_type": row.get("animal_type"), "subtype": row.get("result_status")})
    for row in lab_results:
        history.append({"date": row.get("answer_date"), "operation": "نتیجه آزمایشگاه", "operation_code": "LAB_RESULT", "title": row.get("disease_name"), "detail": row.get("result_status"), "animal_count": row.get("sample_count") or 0, "animal_type": row.get("animal_type"), "subtype": row.get("laboratory_name")})
    for row in occurrences:
        history.append({"date": row.get("start_date"), "operation": "بروز بیماری", "operation_code": "DISEASE_OCCURRENCE", "title": row.get("disease_name"), "detail": row.get("status"), "animal_count": row.get("infected_count") or 0, "animal_type": row.get("animal_type"), "subtype": None})
    for row in disease_reports:
        history.append({"date": row.get("disease_start_date"), "operation": "گزارش بیماری", "operation_code": "DISEASE_REPORT", "title": row.get("disease_name"), "detail": row.get("sampling"), "animal_count": row.get("infected_count") or 0, "animal_type": row.get("animal_type"), "subtype": None})

    history.sort(key=lambda item: (item["date"] is not None, item["date"]), reverse=True)

    sections = {
        "vaccination": vaccination,
        "spraying": spraying,
        "surveillance": surveillance,
        "samples": samples,
        "laboratory_results": lab_results,
        "disease_occurrences": occurrences,
        "disease_reports": disease_reports,
    }

    return {
        "unit": dict(unit),
        "unit_code": unit["unit_code"],
        "unit_name": unit["unit_name"],
        "history": history,
        "sections": sections,
        "summary": {
            "vaccination_operations": len(vaccination),
            "spraying_operations": len(spraying),
            "surveillance_operations": len(surveillance),
            "samples": len(samples),
            "lab_results": len(lab_results),
            "disease_occurrences": len(occurrences),
            "disease_reports": len(disease_reports),
        },
    }
