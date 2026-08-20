from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from app.db.models.gis_county import GISCounty
from app.db.models.gis_disease_occurrence import GISDiseaseOccurrence
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_laboratory_result import GISLaboratoryResult
from app.db.models.gis_send_sample_detail import GISSendSampleDetail
from app.db.models.gis_slaughter_disposal import GISSlaughterDisposal
from app.db.models.gis_spraying import GISSpraying
from app.db.models.gis_surveillance import GISSurveillance
from app.db.models.gis_vaccine_distribution import GISVaccineDistribution
from app.db.models.gis_vaccine_inventory import GISVaccineInventory
from app.db.models.gis_vaccination_performance import GISVaccinationPerformance

ANIMAL_GROUPS = {"گاو": ("cattle_count",), "گاو و گوساله": ("cattle_count",), "گوساله": ("cattle_count",), "گوسفند": ("sheep_count",), "بز": ("goat_count",), "گوسفند و بز": ("sheep_count", "goat_count"), "دام سبک": ("sheep_count", "goat_count"), "بره و بزغاله": ("sheep_count", "goat_count"), "سگ": ("dog_count",), "سگ صاحبدار": ("dog_count",), "سگ بدون صاحب": ("dog_count",), "اسب": ("horse_count",), "تک سمی": ("horse_count",), "شتر": ("camel_count",), "گاومیش": ("buffalo_count",)}
PUBLIC_WORDS = ("دولتی", "رایگان", "عمومی", "شبکه", "اداره")
PRIVATE_WORDS = ("خصوصی", "غیردولتی", "کلینیک", "مرکز خصوصی", "داروخانه")


class GISDiseaseControlDashboardService:
    """Technical management KPIs. Vaccination coverage uses master animal population."""

    @staticmethod
    def _period_filter(query, column, start_date: date | None, end_date: date | None):
        if start_date: query = query.filter(column >= start_date)
        if end_date: query = query.filter(column <= end_date)
        return query

    @staticmethod
    def _scope_query(query, model, province_code: str | None, county_code: str | None):
        if hasattr(model, "province_code") and province_code: query = query.filter(model.province_code == province_code)
        if hasattr(model, "county_code") and county_code: query = query.filter(model.county_code == county_code)
        return query

    @staticmethod
    def _coverage_status(value: float | None) -> str:
        if value is None: return "NO_DATA"
        if value < 50: return "CRITICAL"
        if value < 70: return "WARNING"
        if value < 90: return "ON_TRACK"
        return "EXCELLENT"

    @staticmethod
    def _normalize(value: Any) -> str:
        return str(value or "").strip().replace("ي", "ی").replace("ك", "ک").replace("‌", " ").lower()

    @classmethod
    def _animal_group(cls, value: str | None) -> str | None:
        t = cls._normalize(value)
        if not t: return None
        for key in sorted(ANIMAL_GROUPS, key=len, reverse=True):
            if cls._normalize(key) == t or cls._normalize(key) in t:
                if key in ("گاو", "گاو و گوساله", "گوساله"): return "گاو و گوساله"
                if key == "گوسفند": return "گوسفند"
                if key == "بز": return "بز"
                if key in ("گوسفند و بز", "دام سبک", "بره و بزغاله"): return "گوسفند و بز"
                if key in ("سگ", "سگ صاحبدار", "سگ بدون صاحب"): return "سگ"
                if key in ("اسب", "تک سمی"): return "اسب"
                return key
        return None

    @staticmethod
    def _segment(value: Any) -> str:
        text = str(value or "").strip().lower().replace("ي", "ی").replace("ك", "ک")
        if any(x in text for x in PUBLIC_WORDS): return "public"
        if any(x in text for x in PRIVATE_WORDS): return "private"
        return "other"

    @classmethod
    def _population_map(cls, units: list[GISEpidemiologyUnit]) -> dict[tuple[int, str], int]:
        result = {}
        for u in units:
            result[(u.id, "گاو و گوساله")] = int(u.cattle_count or 0)
            result[(u.id, "گوسفند")] = int(u.sheep_count or 0)
            result[(u.id, "بز")] = int(u.goat_count or 0)
            result[(u.id, "گوسفند و بز")] = int(u.sheep_count or 0) + int(u.goat_count or 0)
            result[(u.id, "اسب")] = int(u.horse_count or 0)
            result[(u.id, "سگ")] = int(u.dog_count or 0)
            result[(u.id, "شتر")] = int(u.camel_count or 0)
            result[(u.id, "گاومیش")] = int(u.buffalo_count or 0)
        return result

    @classmethod
    def _units(cls, db: Session, province_code: str | None, county_code: str | None) -> list[GISEpidemiologyUnit]:
        q = db.query(GISEpidemiologyUnit).filter(GISEpidemiologyUnit.is_active.is_(True))
        if county_code:
            county = db.query(GISCounty).filter(GISCounty.county_code == county_code).first()
            return q.filter(GISEpidemiologyUnit.county_id == county.id).all() if county else []
        if province_code:
            from app.db.models.gis_province import GISProvince
            p = db.query(GISProvince).filter(GISProvince.province_code == province_code).first()
            if not p: return []
            county_ids = [c.id for c in db.query(GISCounty).filter(GISCounty.province_id == p.id).all()]
            return q.filter(GISEpidemiologyUnit.county_id.in_(county_ids)).all() if county_ids else []
        return q.all()

    @classmethod
    def _available_counties(cls, db: Session, province_code: str | None, county_code: str | None):
        q = db.query(GISCounty)
        if county_code:
            q = q.filter(GISCounty.county_code == county_code)
        elif province_code:
            from app.db.models.gis_province import GISProvince
            p = db.query(GISProvince).filter(GISProvince.province_code == province_code).first()
            if p: q = q.filter(GISCounty.province_id == p.id)
        return [{"code": c.county_code, "name": c.county_name} for c in q.order_by(GISCounty.county_name.asc()).all()]

    @classmethod
    def dashboard(cls, db: Session, province_code=None, county_code=None, start_date=None, end_date=None, disease=None, animal_type=None):
        units = cls._units(db, province_code, county_code)
        population = cls._population_map(units)
        vacc_q = cls._period_filter(cls._scope_query(db.query(GISVaccinationPerformance), GISVaccinationPerformance, province_code, county_code), GISVaccinationPerformance.vaccination_date, start_date, end_date)
        if disease: vacc_q = vacc_q.filter(GISVaccinationPerformance.disease_name == disease)
        if animal_type: vacc_q = vacc_q.filter(GISVaccinationPerformance.animal_type == animal_type)
        vacc_rows = vacc_q.order_by(GISVaccinationPerformance.vaccination_date.asc(), GISVaccinationPerformance.id.asc()).all()

        vaccination_by_key = {}
        unit_animal_keys = defaultdict(set)
        monthly = defaultdict(lambda: {"vaccinated": 0, "public": 0, "private": 0})
        map_rows = []
        for row in vacc_rows:
            vaccine = row.vaccine_type or row.disease_name or "نامشخص"
            group = cls._animal_group(row.animal_type)
            item = vaccination_by_key.setdefault(vaccine, {"vaccine": vaccine, "eligible_animals": 0, "vaccinated_animals": 0, "remaining_animals": 0, "coverage_percent": None, "status": "NO_DATA", "animal_types": {}, "public": {"vaccinated_animals": 0, "coverage_vs_population_percent": None}, "private": {"vaccinated_animals": 0, "coverage_vs_population_percent": None}, "other": {"vaccinated_animals": 0, "coverage_vs_population_percent": None}, "target": None, "target_progress_percent": None, "target_available": False})
            vaccinated = int(row.vaccinated_animals or 0)
            segment = cls._segment(row.operation_type)
            item["vaccinated_animals"] += vaccinated
            item[segment]["vaccinated_animals"] += vaccinated
            if group and row.epidemiology_unit_id:
                unit_animal_keys[vaccine].add((row.epidemiology_unit_id, group))
                a = item["animal_types"].setdefault(group, {"animal_type": group, "eligible_animals": 0, "vaccinated_animals": 0, "remaining_animals": 0, "coverage_percent": None})
                a["vaccinated_animals"] += vaccinated
                if row.latitude is not None and row.longitude is not None:
                    map_rows.append({"lat": row.latitude, "lng": row.longitude, "unit_id": row.epidemiology_unit_id, "unit_code": row.epidemiology_unit_code, "unit_name": row.epidemiology_unit_name, "county_code": row.county_code, "county_name": row.county_name, "operation": "vaccination", "vaccine": vaccine, "animal_type": group, "value": vaccinated})
            if row.vaccination_date:
                key = row.vaccination_date.strftime("%Y-%m")
                monthly[key]["vaccinated"] += vaccinated
                monthly[key][segment] += vaccinated

        for vaccine, item in vaccination_by_key.items():
            eligible = sum(population.get(key, 0) for key in unit_animal_keys[vaccine])
            item["eligible_animals"] = eligible
            item["remaining_animals"] = max(eligible - item["vaccinated_animals"], 0)
            item["coverage_percent"] = round(item["vaccinated_animals"] / eligible * 100, 2) if eligible else None
            item["status"] = cls._coverage_status(item["coverage_percent"])
            for segment in ("public", "private", "other"):
                item[segment]["coverage_vs_population_percent"] = round(item[segment]["vaccinated_animals"] / eligible * 100, 2) if eligible else None
            for group, a in item["animal_types"].items():
                a_keys = {key for key in unit_animal_keys[vaccine] if key[1] == group}
                a["eligible_animals"] = sum(population.get(key, 0) for key in a_keys)
                a["remaining_animals"] = max(a["eligible_animals"] - a["vaccinated_animals"], 0)
                a["coverage_percent"] = round(a["vaccinated_animals"] / a["eligible_animals"] * 100, 2) if a["eligible_animals"] else None
            item["animal_types"] = list(item["animal_types"].values())

        disease_q = cls._period_filter(cls._scope_query(db.query(GISDiseaseOccurrence), GISDiseaseOccurrence, province_code, county_code), GISDiseaseOccurrence.report_date, start_date, end_date)
        if disease: disease_q = disease_q.filter(GISDiseaseOccurrence.disease_name == disease)
        if animal_type: disease_q = disease_q.filter(GISDiseaseOccurrence.animal_type == animal_type)
        disease_rows = disease_q.all()
        disease_summary = {}
        for row in disease_rows:
            name = row.disease_name or "نامشخص"
            x = disease_summary.setdefault(name, {"disease": name, "outbreaks": 0, "exposed": 0, "infected": 0, "deaths": 0, "slaughtered": 0, "sampled": 0})
            x["outbreaks"] += 1; x["exposed"] += int(row.exposed_count or 0); x["infected"] += int(row.infected_count or 0); x["deaths"] += int(row.dead_count or 0); x["slaughtered"] += int(row.slaughtered_count or 0); x["sampled"] += 1 if row.sample_taken else 0
            if row.latitude is not None and row.longitude is not None: map_rows.append({"lat": row.latitude, "lng": row.longitude, "unit_id": row.epidemiology_unit_id, "unit_code": row.epidemiology_unit_code, "unit_name": row.epidemiology_unit_name, "county_code": row.county_code, "county_name": row.county_name, "operation": "disease", "disease": row.disease_name, "animal_type": row.animal_type, "value": int(row.infected_count or 0)})
        for x in disease_summary.values():
            x["attack_rate_percent"] = round(x["infected"] / x["exposed"] * 100, 2) if x["exposed"] else 0; x["case_fatality_percent"] = round(x["deaths"] / x["infected"] * 100, 2) if x["infected"] else 0

        surv_q = cls._period_filter(cls._scope_query(db.query(GISSurveillance), GISSurveillance, province_code, county_code), GISSurveillance.surveillance_date, start_date, end_date)
        if animal_type: surv_q = surv_q.filter(GISSurveillance.animal_type == animal_type)
        surveillance_rows = surv_q.all(); surveillance = {"operations": len(surveillance_rows), "animals_examined": sum(int(r.total_animals or 0) for r in surveillance_rows), "positive": sum(int(r.positive or 0) for r in surveillance_rows), "negative": sum(int(r.negative or 0) for r in surveillance_rows), "suspected": sum(int(r.suspected or 0) for r in surveillance_rows)}; surveillance["positive_rate_percent"] = round(surveillance["positive"] / surveillance["animals_examined"] * 100, 2) if surveillance["animals_examined"] else 0
        samples = cls._period_filter(cls._scope_query(db.query(GISSendSampleDetail), GISSendSampleDetail, province_code, county_code), GISSendSampleDetail.sampling_date, start_date, end_date).all()
        lab_rows = cls._period_filter(cls._scope_query(db.query(GISLaboratoryResult), GISLaboratoryResult, province_code, county_code), GISLaboratoryResult.sampling_date, start_date, end_date).all()
        lab_status = defaultdict(int)
        for r in lab_rows: lab_status[(r.result_status or "نامشخص").strip()] += int(r.sample_count or 0)
        spraying_rows = cls._period_filter(cls._scope_query(db.query(GISSpraying), GISSpraying, province_code, county_code), GISSpraying.spraying_date, start_date, end_date).all()
        slaughter_rows = cls._period_filter(cls._scope_query(db.query(GISSlaughterDisposal), GISSlaughterDisposal, province_code, county_code), GISSlaughterDisposal.action_date, start_date, end_date).all()
        distribution_rows = cls._period_filter(cls._scope_query(db.query(GISVaccineDistribution), GISVaccineDistribution, province_code, county_code), GISVaccineDistribution.distribution_date, start_date, end_date).all()
        inventory_rows = cls._scope_query(db.query(GISVaccineInventory), GISVaccineInventory, province_code, county_code).all()
        today = end_date or date.today(); expiring_30 = sum(int(r.package_count or 0) for r in inventory_rows if r.expiration_date and 0 <= (r.expiration_date - today).days <= 30); expiring_60 = sum(int(r.package_count or 0) for r in inventory_rows if r.expiration_date and 0 <= (r.expiration_date - today).days <= 60)
        population_by_animal = {"گاو و گوساله": sum(int(u.cattle_count or 0) for u in units), "گوسفند": sum(int(u.sheep_count or 0) for u in units), "بز": sum(int(u.goat_count or 0) for u in units), "اسب": sum(int(u.horse_count or 0) for u in units), "سگ": sum(int(u.dog_count or 0) for u in units), "شتر": sum(int(u.camel_count or 0) for u in units), "گاومیش": sum(int(u.buffalo_count or 0) for u in units)}
        total_vaccinated = sum(x["vaccinated_animals"] for x in vaccination_by_key.values()); public_vaccinated = sum(x["public"]["vaccinated_animals"] for x in vaccination_by_key.values()); private_vaccinated = sum(x["private"]["vaccinated_animals"] for x in vaccination_by_key.values())
        map_points = []; seen = set()
        for p in map_rows:
            key = (p.get("unit_id"), p.get("operation"), p.get("vaccine") or p.get("disease"), p.get("animal_type"))
            if key in seen: continue
            seen.add(key)
            if p.get("operation") == "vaccination":
                eligible = population.get((p.get("unit_id"), p.get("animal_type")), 0); p["coverage_percent"] = round(p["value"] / eligible * 100, 2) if eligible else None
            map_points.append(p)
        return {"scope": {"province_code": province_code, "county_code": county_code}, "available_counties": cls._available_counties(db, province_code, county_code), "period": {"start": start_date.isoformat() if start_date else None, "end": end_date.isoformat() if end_date else None}, "population": {"by_animal_type": population_by_animal, "total": sum(population_by_animal.values())}, "vaccination": list(vaccination_by_key.values()), "vaccination_overview": {"vaccinated_animals": total_vaccinated, "public_vaccinated": public_vaccinated, "private_vaccinated": private_vaccinated, "other_vaccinated": max(total_vaccinated - public_vaccinated - private_vaccinated, 0), "note": "پوشش کلی بین واکسن‌های مختلف تجمیع نمی‌شود؛ پوشش فقط در سطح هر واکسن و گروه دام معتبر است."}, "vaccination_monthly": [{"month": k, **v} for k, v in sorted(monthly.items())], "disease": list(disease_summary.values()), "surveillance": surveillance, "samples": {"sent_operations": len(samples), "sample_count": sum(int(r.sample_count or 0) for r in samples), "without_result": sum(1 for r in samples if not r.result_status)}, "laboratory": {"results": len(lab_rows), "sample_count": sum(int(r.sample_count or 0) for r in lab_rows), "by_status": dict(lab_status)}, "parasitic_control": {"operations": len(spraying_rows), "units": len({r.epidemiology_unit_id for r in spraying_rows if r.epidemiology_unit_id}), "animals": sum(int(r.sprayed_animal_count or 0) for r in spraying_rows), "area": float(sum(r.sprayed_area or 0 for r in spraying_rows))}, "control_actions": {"operations": len(slaughter_rows), "positive": sum(int(r.positive_count or 0) for r in slaughter_rows), "slaughtered": sum(int(r.slaughtered_count or 0) for r in slaughter_rows), "destroyed": sum(int(r.destroyed_count or 0) for r in slaughter_rows), "dead": sum(int(r.dead_count or 0) for r in slaughter_rows)}, "vaccine_supply": {"distribution_operations": len(distribution_rows), "distributed_packages": sum(int(r.package_count or 0) for r in distribution_rows), "inventory_rows": len(inventory_rows), "expiring_30_days_packages": expiring_30, "expiring_60_days_packages": expiring_60}, "management_alerts": cls._alerts(vaccination_by_key, disease_summary, samples, inventory_rows, slaughter_rows, today), "map_points": map_points, "economic": {"status": "not_available", "budget": None, "technical_cost": None, "avoided_loss": None, "roi": None, "note": "ساختار اقتصادی آماده اتصال است؛ پس از ایجاد جداول بودجه، هزینه و ارزش دام محاسبه خواهد شد."}}

    @staticmethod
    def _alerts(vaccination, diseases, samples, inventory, slaughter, today):
        alerts = []
        for item in vaccination.values():
            coverage = item.get("coverage_percent")
            if coverage is not None and coverage < 50: alerts.append({"level": "CRITICAL", "type": "vaccination", "title": f"پوشش {item['vaccine']} کمتر از ۵۰٪ است", "value": coverage})
            elif coverage is not None and coverage < 70: alerts.append({"level": "WARNING", "type": "vaccination", "title": f"پوشش {item['vaccine']} نیازمند توجه است", "value": coverage})
        for item in diseases.values():
            if item["infected"] > 0: alerts.append({"level": "CRITICAL", "type": "disease", "title": f"گزارش {item['disease']} با {item['infected']:,} دام مبتلا", "value": item["infected"]})
        pending = sum(1 for r in samples if not r.result_status)
        if pending: alerts.append({"level": "WARNING", "type": "sample", "title": f"{pending} مورد نمونه بدون نتیجه ثبت‌شده", "value": pending})
        expiring = sum(int(r.package_count or 0) for r in inventory if r.expiration_date and 0 <= (r.expiration_date - today).days <= 30)
        if expiring: alerts.append({"level": "WARNING", "type": "inventory", "title": f"{expiring:,} بسته واکسن در کمتر از ۳۰ روز منقضی می‌شود", "value": expiring})
        uncovered = [r for r in slaughter if (r.positive_count or 0) > 0 and (r.destroyed_count or 0) + (r.slaughtered_count or 0) == 0]
        if uncovered: alerts.append({"level": "CRITICAL", "type": "control_action", "title": f"{len(uncovered)} مورد مثبت بدون اقدام ثبت شده", "value": len(uncovered)})
        return alerts
