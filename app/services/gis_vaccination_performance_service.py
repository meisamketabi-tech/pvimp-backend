from typing import Optional, Dict, Any

from sqlalchemy.orm import Session

from app.db.models.gis_vaccination_performance import GISVaccinationPerformance


class GISVaccinationPerformanceService:

    @staticmethod
    def _effective_eligible(row) -> int:
        eligible = int(row.eligible_animals or 0)

        if eligible > 0:
            return eligible

        total = int(row.total_animals or 0)

        if total > 0:
            return total

        animal_count = int(row.animal_count or 0)

        if animal_count > 0:
            return animal_count

        return 0

    @staticmethod
    def get_vaccine_summary(
        db: Session,
        vaccine: str,
        province_code: Optional[str] = None,
    ) -> Dict[str, Any]:

        query = db.query(
            GISVaccinationPerformance
        ).filter(
            GISVaccinationPerformance.vaccine_type == vaccine
        )

        if province_code:
            query = query.filter(
                GISVaccinationPerformance.province_code
                == province_code
            )

        rows = query.all()

        total_eligible = sum(
            GISVaccinationPerformanceService._effective_eligible(row)
            for row in rows
        )

        total_vaccinated = sum(
            int(row.vaccinated_animals or 0)
            for row in rows
        )

        coverage = (
            (total_vaccinated / total_eligible) * 100
            if total_eligible
            else 0
        )

        counties = {}

        for row in rows:

            county_key = (
                row.county_code
                or row.county_name
                or "UNKNOWN"
            )

            if county_key not in counties:
                counties[county_key] = {
                    "county_code": row.county_code,
                    "county_name": row.county_name,
                    "eligible_animals": 0,
                    "vaccinated_animals": 0,
                    "coverage_percent": 0,
                    "units": {},
                }

            county = counties[county_key]

            effective_eligible = (
                GISVaccinationPerformanceService
                ._effective_eligible(row)
            )

            vaccinated = int(
                row.vaccinated_animals or 0
            )

            county["eligible_animals"] += (
                effective_eligible
            )

            county["vaccinated_animals"] += (
                vaccinated
            )

            unit_key = (
                row.epidemiology_unit_id
                or row.epidemiology_unit_code
                or row.epidemiology_unit_name
                or "UNKNOWN"
            )

            if unit_key not in county["units"]:
                county["units"][unit_key] = {
                    "epidemiology_unit_id":
                        row.epidemiology_unit_id,
                    "epidemiology_unit_code":
                        row.epidemiology_unit_code,
                    "epidemiology_unit_name":
                        row.epidemiology_unit_name,
                    "epidemiology_unit_type":
                        row.epidemiology_unit_type,
                    "eligible_animals": 0,
                    "vaccinated_animals": 0,
                    "coverage_percent": 0,
                }

            unit = county["units"][unit_key]

            unit["eligible_animals"] += (
                effective_eligible
            )

            unit["vaccinated_animals"] += (
                vaccinated
            )

        for county in counties.values():

            eligible = county["eligible_animals"]
            vaccinated = county["vaccinated_animals"]

            county["coverage_percent"] = (
                round(
                    (vaccinated / eligible) * 100,
                    2,
                )
                if eligible
                else 0
            )

            county["remaining_animals"] = max(
                eligible - vaccinated,
                0,
            )

            county["units"] = list(
                county["units"].values()
            )

            for unit in county["units"]:

                unit_eligible = unit[
                    "eligible_animals"
                ]

                unit_vaccinated = unit[
                    "vaccinated_animals"
                ]

                unit["coverage_percent"] = (
                    round(
                        (
                            unit_vaccinated
                            / unit_eligible
                        ) * 100,
                        2,
                    )
                    if unit_eligible
                    else 0
                )

                unit["remaining_animals"] = max(
                    unit_eligible
                    - unit_vaccinated,
                    0,
                )

        return {
            "vaccine": vaccine,
            "province_code": province_code,
            "eligible_animals": total_eligible,
            "vaccinated_animals": total_vaccinated,
            "coverage_percent": round(
                coverage,
                2,
            ),
            "remaining_animals": max(
                total_eligible
                - total_vaccinated,
                0,
            ),
            "counties": list(
                counties.values()
            ),
        }

    @staticmethod
    def get_county_details(
        db: Session,
        vaccine: str,
        county_code: str,
    ) -> Dict[str, Any]:

        rows = (
            db.query(
                GISVaccinationPerformance
            )
            .filter(
                GISVaccinationPerformance.vaccine_type
                == vaccine,
                GISVaccinationPerformance.county_code
                == county_code,
            )
            .order_by(
                GISVaccinationPerformance
                .vaccination_date
                .desc(),
                GISVaccinationPerformance
                .registration_date
                .desc(),
            )
            .all()
        )

        units = {}

        for row in rows:

            key = (
                row.epidemiology_unit_id
                or row.epidemiology_unit_code
                or row.epidemiology_unit_name
                or "UNKNOWN"
            )

            if key not in units:
                units[key] = {
                    "epidemiology_unit_id":
                        row.epidemiology_unit_id,
                    "epidemiology_unit_code":
                        row.epidemiology_unit_code,
                    "epidemiology_unit_name":
                        row.epidemiology_unit_name,
                    "epidemiology_unit_type":
                        row.epidemiology_unit_type,
                    "latitude":
                        row.latitude,
                    "longitude":
                        row.longitude,
                    "eligible_animals": 0,
                    "vaccinated_animals": 0,
                    "coverage_percent": 0,
                }

            unit = units[key]

            unit["eligible_animals"] += (
                GISVaccinationPerformanceService
                ._effective_eligible(row)
            )

            unit["vaccinated_animals"] += int(
                row.vaccinated_animals or 0
            )

        total_eligible = sum(
            unit["eligible_animals"]
            for unit in units.values()
        )

        total_vaccinated = sum(
            unit["vaccinated_animals"]
            for unit in units.values()
        )

        for unit in units.values():

            eligible = unit[
                "eligible_animals"
            ]

            vaccinated = unit[
                "vaccinated_animals"
            ]

            unit["coverage_percent"] = (
                round(
                    (vaccinated / eligible) * 100,
                    2,
                )
                if eligible
                else 0
            )

            unit["remaining_animals"] = max(
                eligible - vaccinated,
                0,
            )

        return {
            "vaccine": vaccine,
            "county_code": county_code,
            "eligible_animals": total_eligible,
            "vaccinated_animals": total_vaccinated,
            "coverage_percent": (
                round(
                    (
                        total_vaccinated
                        / total_eligible
                    ) * 100,
                    2,
                )
                if total_eligible
                else 0
            ),
            "remaining_animals": max(
                total_eligible
                - total_vaccinated,
                0,
            ),
            "units": list(
                units.values()
            ),
        }

    @staticmethod
    def get_unit_details(
        db: Session,
        vaccine: str,
        epidemiology_unit_id: int,
    ) -> Dict[str, Any]:

        rows = (
            db.query(
                GISVaccinationPerformance
            )
            .filter(
                GISVaccinationPerformance.vaccine_type
                == vaccine,
                GISVaccinationPerformance
                .epidemiology_unit_id
                == epidemiology_unit_id,
            )
            .order_by(
                GISVaccinationPerformance
                .vaccination_date
                .desc(),
                GISVaccinationPerformance
                .registration_date
                .desc(),
                GISVaccinationPerformance
                .id
                .desc(),
            )
            .all()
        )

        if not rows:
            return {
                "vaccine": vaccine,
                "epidemiology_unit_id":
                    epidemiology_unit_id,
                "summary": {
                    "eligible_animals": 0,
                    "vaccinated_animals": 0,
                    "remaining_animals": 0,
                    "coverage_percent": 0,
                },
                "operations": [],
            }

        first = rows[0]

        total_eligible = sum(
            GISVaccinationPerformanceService
            ._effective_eligible(row)
            for row in rows
        )

        total_vaccinated = sum(
            int(row.vaccinated_animals or 0)
            for row in rows
        )

        operations = []

        for row in rows:

            effective_eligible = (
                GISVaccinationPerformanceService
                ._effective_eligible(row)
            )

            vaccinated = int(
                row.vaccinated_animals or 0
            )

            operations.append({
                "id": row.id,

                "control_action_vaccine_vcode":
                    row.control_action_vaccine_vcode,

                "vaccination_no":
                    row.vaccination_no,

                "province_code":
                    row.province_code,

                "province_name":
                    row.province_name,

                "county_code":
                    row.county_code,

                "county_name":
                    row.county_name,

                "epidemiology_unit_id":
                    row.epidemiology_unit_id,

                "epidemiology_unit_code":
                    row.epidemiology_unit_code,

                "epidemiology_unit_name":
                    row.epidemiology_unit_name,

                "epidemiology_unit_type":
                    row.epidemiology_unit_type,

                "latitude":
                    row.latitude,

                "longitude":
                    row.longitude,

                "vaccination_center_name":
                    row.vaccination_center_name,

                "vaccination_center_code":
                    row.vaccination_center_code,

                "vaccine_type":
                    row.vaccine_type,

                "vaccine_brand":
                    row.vaccine_brand,

                "manufacturer":
                    row.manufacturer,

                "vaccine_category":
                    row.vaccine_category,

                "batch_number":
                    row.batch_number,

                "animal_type":
                    row.animal_type,

                "vaccination_date":
                    row.vaccination_date,

                "registration_date":
                    row.registration_date,

                "rappel_vaccination":
                    row.rappel_vaccination,

                "operation_type":
                    row.operation_type,

                "total_animals":
                    row.total_animals,

                "animal_count":
                    row.animal_count,

                "eligible_animals":
                    effective_eligible,

                "vaccinated_animals":
                    vaccinated,

                "remaining_animals":
                    max(
                        effective_eligible
                        - vaccinated,
                        0,
                    ),

                "age_group":
                    row.age_group,

                "dose_per_vial":
                    row.dose_per_vial,

                "package_count":
                    row.package_count,

                "disease_name":
                    row.disease_name,

                "shock_after_injection":
                    row.shock_after_injection,

                "shock_count":
                    row.shock_count,

                "death_count":
                    row.death_count,

                "abortion":
                    row.abortion,

                "abortion_count":
                    row.abortion_count,

                "hypersensitivity":
                    row.hypersensitivity,

                "hypersensitivity_count":
                    row.hypersensitivity_count,

                "local_complication":
                    row.local_complication,

                "local_complication_count":
                    row.local_complication_count,
            })

        return {
            "vaccine": vaccine,

            "epidemiology_unit": {
                "id":
                    first.epidemiology_unit_id,

                "code":
                    first.epidemiology_unit_code,

                "name":
                    first.epidemiology_unit_name,

                "type":
                    first.epidemiology_unit_type,

                "latitude":
                    first.latitude,

                "longitude":
                    first.longitude,
            },

            "summary": {
                "eligible_animals":
                    total_eligible,

                "vaccinated_animals":
                    total_vaccinated,

                "remaining_animals":
                    max(
                        total_eligible
                        - total_vaccinated,
                        0,
                    ),

                "coverage_percent": (
                    round(
                        (
                            total_vaccinated
                            / total_eligible
                        ) * 100,
                        2,
                    )
                    if total_eligible
                    else 0
                ),
            },

            "operations": operations,
        }
