from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.gis_disease_occurrence import GISDiseaseOccurrence
from app.db.models.gis_disease_report import GISDiseaseReport
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_laboratory_result import GISLaboratoryResult
from app.db.models.gis_send_sample_detail import GISSendSampleDetail
from app.db.models.gis_slaughter_disposal import GISSlaughterDisposal
from app.db.models.gis_spraying import GISSpraying
from app.db.models.gis_surveillance import GISSurveillance
from app.db.models.gis_vaccine_distribution import GISVaccineDistribution
from app.db.models.gis_vaccine_inventory import GISVaccineInventory
from app.db.models.gis_vaccination_performance import GISVaccinationPerformance


class GISDiseaseControlDashboardService:
    """Read-only management KPIs for the provincial animal-disease-control unit.

    The service deliberately keeps technical KPIs separate from future financial KPIs.
    Financial fields are exposed as null/placeholders until budget/cost tables exist.
    """

    @staticmethod
    def _period_filter(query, column, start_date: date | None, end_date: date | None):
        if start_date:
            query = query.filter(column >= start_date)
        if end_date:
            query = query.filter(column <= end_date)
        return query

    @staticmethod
    def _scope_query(query, model, province_code: str | None, county_code: str | None):
        if hasattr(model, "province_code") and province_code:
            query = query.filter(model.province_code == province_code)
        if hasattr(model, "county_code") and county_code:
            query = query.filter(model.county_code == county_code)
        return query

    @staticmethod
    def _coverage_status(value: float | None) -> str:
        if value is None:
            return "NO_DATA"
        if value < 50:
            return "CRITICAL"
        if value < 70:
            return "WARNING"
        if value < 90:
            return "ON_TRACK"
        return "EXCELLENT"

    @classmethod
    def dashboard(
        cls,
        db: Session,
        province_code: str | None = None,
        county_code: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        disease: str | None = None,
        animal_type: str | None = None,
    ) -> dict[str, Any]:
        units_q = db.query(GISEpidemiologyUnit).filter(GISEpidemiologyUnit.is_active.is_(True))
        if province_code:
            units_q = units_q.filter(GISEpidemiologyUnit.province_id.isnot(None))
        if county_code:
            # County code is not stored on the unit model; operational tables carry it.
            unit_ids = [r[0] for r in db.query(GISVaccinationPerformance.epidemiology_unit_id)
                        .filter(GISVaccinationPerformance.county_code == county_code)
                        .distinct().all() if r[0] is not None]
            if unit_ids:
                units_q = units_q.filter(GISEpidemiologyUnit.id.in_(unit_ids))
            else:
                units_q = units_q.filter(False)

        units = units_q.all()

        animal_population = {
            "گوسفند": sum(int(u.sheep_count or 0) for u in units),
            "گاو": sum(int(u.cattle_count or 0) for u in units),
            "بز": sum(int(u.goat_count or 0) for u in units),
            "اسب": sum(int(u.horse_count or 0) for u in units),
            "سگ": sum(int(u.dog_count or 0) for u in units),
            "شتر": sum(int(u.camel_count or 0) for u in units),
            "گاومیش": sum(int(u.buffalo_count or 0) for u in units),
        }

        vacc_q = db.query(GISVaccinationPerformance).filter(GISVaccinationPerformance.id.isnot(None))
        vacc_q = cls._scope_query(vacc_q, GISVaccinationPerformance, province_code, county_code)
        vacc_q = cls._period_filter(vacc_q, GISVaccinationPerformance.vaccination_date, start_date, end_date)
        if disease:
            vacc_q = vacc_q.filter(GISVaccinationPerformance.disease_name == disease)
        if animal_type:
            vacc_q = vacc_q.filter(GISVaccinationPerformance.animal_type == animal_type)
        vacc_rows = vacc_q.order_by(GISVaccinationPerformance.vaccination_date.desc(), GISVaccinationPerformance.id.desc()).all()

        # Coverage is based on the latest operation per unit + vaccine + animal type,
        # not on the number of database records. This prevents historical rows from
        # inflating the denominator/numerator.
        latest: dict[tuple[Any, Any, Any], GISVaccinationPerformance] = {}
        for row in vacc_rows:
            key = (row.epidemiology_unit_id or row.epidemiology_unit_code, row.vaccine_type, row.animal_type)
            if key not in latest:
                latest[key] = row

        vaccination_by_key: dict[str, dict[str, Any]] = {}
        for row in latest.values():
            vaccine = row.vaccine_type or row.disease_name or "نامشخص"
            item = vaccination_by_key.setdefault(vaccine, {
                "vaccine": vaccine,
                "eligible_animals": 0,
                "vaccinated_animals": 0,
                "remaining_animals": 0,
                "coverage_percent": 0,
                "animal_types": {},
            })
            eligible = int(row.eligible_animals or row.total_animals or row.animal_count or 0)
            vaccinated = int(row.vaccinated_animals or 0)
            item["eligible_animals"] += eligible
            item["vaccinated_animals"] += vaccinated
            animal = row.animal_type or "نامشخص"
            a = item["animal_types"].setdefault(animal, {"animal_type": animal, "eligible_animals": 0, "vaccinated_animals": 0})
            a["eligible_animals"] += eligible
            a["vaccinated_animals"] += vaccinated

        for item in vaccination_by_key.values():
            item["remaining_animals"] = max(item["eligible_animals"] - item["vaccinated_animals"], 0)
            item["coverage_percent"] = round(item["vaccinated_animals"] / item["eligible_animals"] * 100, 2) if item["eligible_animals"] else 0
            item["status"] = cls._coverage_status(item["coverage_percent"])
            for a in item["animal_types"].values():
                a["remaining_animals"] = max(a["eligible_animals"] - a["vaccinated_animals"], 0)
                a["coverage_percent"] = round(a["vaccinated_animals"] / a["eligible_animals"] * 100, 2) if a["eligible_animals"] else 0
                a["status"] = cls._coverage_status(a["coverage_percent"])
            item["animal_types"] = list(item["animal_types"].values())

        disease_q = db.query(GISDiseaseOccurrence)
        disease_q = cls._scope_query(disease_q, GISDiseaseOccurrence, province_code, county_code)
        disease_q = cls._period_filter(disease_q, GISDiseaseOccurrence.report_date, start_date, end_date)
        if disease:
            disease_q = disease_q.filter(GISDiseaseOccurrence.disease_name == disease)
        if animal_type:
            disease_q = disease_q.filter(GISDiseaseOccurrence.animal_type == animal_type)
        disease_rows = disease_q.all()

        disease_summary: dict[str, dict[str, Any]] = {}
        for row in disease_rows:
            name = row.disease_name or "نامشخص"
            x = disease_summary.setdefault(name, {"disease": name, "outbreaks": 0, "exposed": 0, "infected": 0, "deaths": 0, "slaughtered": 0, "sampled": 0})
            x["outbreaks"] += 1
            x["exposed"] += int(row.exposed_count or 0)
            x["infected"] += int(row.infected_count or 0)
            x["deaths"] += int(row.dead_count or 0)
            x["slaughtered"] += int(row.slaughtered_count or 0)
            x["sampled"] += 1 if row.sample_taken else 0

        for x in disease_summary.values():
            x["attack_rate_percent"] = round(x["infected"] / x["exposed"] * 100, 2) if x["exposed"] else 0
            x["case_fatality_percent"] = round(x["deaths"] / x["infected"] * 100, 2) if x["infected"] else 0

        surv_q = db.query(GISSurveillance)
        surv_q = cls._scope_query(surv_q, GISSurveillance, province_code, county_code)
        surv_q = cls._period_filter(surv_q, GISSurveillance.surveillance_date, start_date, end_date)
        if animal_type:
            surv_q = surv_q.filter(GISSurveillance.animal_type == animal_type)
        surveillance_rows = surv_q.all()
        surveillance = {
            "operations": len(surveillance_rows),
            "animals_examined": sum(int(r.total_animals or 0) for r in surveillance_rows),
            "positive": sum(int(r.positive or 0) for r in surveillance_rows),
            "negative": sum(int(r.negative or 0) for r in surveillance_rows),
            "suspected": sum(int(r.suspected or 0) for r in surveillance_rows),
        }
        surveillance["positive_rate_percent"] = round(surveillance["positive"] / surveillance["animals_examined"] * 100, 2) if surveillance["animals_examined"] else 0

        sample_q = db.query(GISSendSampleDetail)
        sample_q = cls._scope_query(sample_q, GISSendSampleDetail, province_code, county_code)
        sample_q = cls._period_filter(sample_q, GISSendSampleDetail.sampling_date, start_date, end_date)
        samples = sample_q.all()

        lab_q = db.query(GISLaboratoryResult)
        lab_q = cls._scope_query(lab_q, GISLaboratoryResult, province_code, county_code)
        lab_q = cls._period_filter(lab_q, GISLaboratoryResult.sampling_date, start_date, end_date)
        lab_rows = lab_q.all()
        lab_status = defaultdict(int)
        for r in lab_rows:
            lab_status[(r.result_status or "نامشخص").strip()] += int(r.sample_count or 0)

        spraying_q = db.query(GISSpraying)
        spraying_q = cls._scope_query(spraying_q, GISSpraying, province_code, county_code)
        spraying_q = cls._period_filter(spraying_q, GISSpraying.spraying_date, start_date, end_date)
        spraying_rows = spraying_q.all()

        slaughter_q = db.query(GISSlaughterDisposal)
        slaughter_q = cls._scope_query(slaughter_q, GISSlaughterDisposal, province_code, county_code)
        slaughter_q = cls._period_filter(slaughter_q, GISSlaughterDisposal.action_date, start_date, end_date)
        slaughter_rows = slaughter_q.all()

        distribution_q = db.query(GISVaccineDistribution)
        distribution_q = cls._scope_query(distribution_q, GISVaccineDistribution, province_code, county_code)
        distribution_q = cls._period_filter(distribution_q, GISVaccineDistribution.distribution_date, start_date, end_date)
        distribution_rows = distribution_q.all()

        inventory_q = db.query(GISVaccineInventory)
        inventory_q = cls._scope_query(inventory_q, GISVaccineInventory, province_code, county_code)
        inventory_rows = inventory_q.all()
        today = end_date or date.today()
        expiring_30 = sum(int(r.package_count or 0) for r in inventory_rows if r.expiration_date and 0 <= (r.expiration_date - today).days <= 30)
        expiring_60 = sum(int(r.package_count or 0) for r in inventory_rows if r.expiration_date and 0 <= (r.expiration_date - today).days <= 60)

        map_points = []
        point_sources = latest.values()
        for row in point_sources:
            if row.latitude is None or row.longitude is None:
                continue
            map_points.append({
                "lat": row.latitude,
                "lng": row.longitude,
                "unit_id": row.epidemiology_unit_id,
                "unit_code": row.epidemiology_unit_code,
                "unit_name": row.epidemiology_unit_name,
                "county_code": row.county_code,
                "county_name": row.county_name,
                "operation": "vaccination",
                "vaccine": row.vaccine_type,
                "animal_type": row.animal_type,
                "value": int(row.vaccinated_animals or 0),
                "coverage_percent": round((int(row.vaccinated_animals or 0) / int(row.eligible_animals or row.total_animals or row.animal_count or 0)) * 100, 2) if int(row.eligible_animals or row.total_animals or row.animal_count or 0) else 0,
            })
        for row in disease_rows:
            if row.latitude is None or row.longitude is None:
                continue
            map_points.append({
                "lat": row.latitude,
                "lng": row.longitude,
                "unit_id": row.epidemiology_unit_id,
                "unit_code": row.epidemiology_unit_code,
                "unit_name": row.epidemiology_unit_name,
                "county_code": row.county_code,
                "county_name": row.county_name,
                "operation": "disease",
                "disease": row.disease_name,
                "animal_type": row.animal_type,
                "value": int(row.infected_count or 0),
            })

        return {
            "scope": {"province_code": province_code, "county_code": county_code},
            "period": {"start": start_date.isoformat() if start_date else None, "end": end_date.isoformat() if end_date else None},
            "population": {"by_animal_type": animal_population, "total": sum(animal_population.values())},
            "vaccination": list(vaccination_by_key.values()),
            "disease": list(disease_summary.values()),
            "surveillance": surveillance,
            "samples": {
                "sent_operations": len(samples),
                "sample_count": sum(int(r.sample_count or 0) for r in samples),
                "without_result": sum(1 for r in samples if not r.result_status),
            },
            "laboratory": {
                "results": len(lab_rows),
                "sample_count": sum(int(r.sample_count or 0) for r in lab_rows),
                "by_status": dict(lab_status),
            },
            "parasitic_control": {
                "operations": len(spraying_rows),
                "units": len({r.epidemiology_unit_id for r in spraying_rows if r.epidemiology_unit_id}),
                "animals": sum(int(r.sprayed_animal_count or 0) for r in spraying_rows),
                "area": float(sum(r.sprayed_area or 0 for r in spraying_rows)),
            },
            "control_actions": {
                "operations": len(slaughter_rows),
                "positive": sum(int(r.positive_count or 0) for r in slaughter_rows),
                "slaughtered": sum(int(r.slaughtered_count or 0) for r in slaughter_rows),
                "destroyed": sum(int(r.destroyed_count or 0) for r in slaughter_rows),
                "dead": sum(int(r.dead_count or 0) for r in slaughter_rows),
            },
            "vaccine_supply": {
                "distribution_operations": len(distribution_rows),
                "distributed_packages": sum(int(r.package_count or 0) for r in distribution_rows),
                "inventory_rows": len(inventory_rows),
                "expiring_30_days_packages": expiring_30,
                "expiring_60_days_packages": expiring_60,
            },
            "management_alerts": cls._alerts(vaccination_by_key, disease_summary, surveillance, samples, lab_rows, inventory_rows, slaughter_rows, today),
            "map_points": map_points,
            "economic": {
                "status": "not_available",
                "budget": None,
                "technical_cost": None,
                "avoided_loss": None,
                "roi": None,
                "note": "ساختار اقتصادی آماده اتصال است؛ پس از ایجاد جداول بودجه، هزینه و ارزش دام محاسبه خواهد شد.",
            },
        }

    @staticmethod
    def _alerts(vaccination, diseases, surveillance, samples, labs, inventory, slaughter, today):
        alerts = []
        for item in vaccination.values():
            if item["eligible_animals"] and item["coverage_percent"] < 50:
                alerts.append({"level": "CRITICAL", "type": "vaccination", "title": f"پوشش {item['vaccine']} کمتر از ۵۰٪ است", "value": item["coverage_percent"]})
            elif item["eligible_animals"] and item["coverage_percent"] < 70:
                alerts.append({"level": "WARNING", "type": "vaccination", "title": f"پوشش {item['vaccine']} نیازمند توجه است", "value": item["coverage_percent"]})
        for item in diseases.values():
            if item["infected"] > 0:
                alerts.append({"level": "CRITICAL", "type": "disease", "title": f"کانون/گزارش فعال {item['disease']} با {item['infected']:,} دام مبتلا", "value": item["infected"]})
        pending = sum(1 for r in samples if not r.result_status)
        if pending:
            alerts.append({"level": "WARNING", "type": "sample", "title": f"{pending} مورد نمونه بدون نتیجه ثبت‌شده", "value": pending})
        expiring = sum(int(r.package_count or 0) for r in inventory if r.expiration_date and 0 <= (r.expiration_date - today).days <= 30)
        if expiring:
            alerts.append({"level": "WARNING", "type": "inventory", "title": f"{expiring:,} بسته واکسن در کمتر از ۳۰ روز منقضی می‌شود", "value": expiring})
        uncovered = [r for r in slaughter if (r.positive_count or 0) > 0 and (r.destroyed_count or 0) + (r.slaughtered_count or 0) == 0]
        if uncovered:
            alerts.append({"level": "CRITICAL", "type": "control_action", "title": f"{len(uncovered)} مورد مثبت بدون اقدام کشتار/معدوم‌سازی ثبت شده", "value": len(uncovered)})
        return alerts
