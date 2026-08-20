from __future__ import annotations

import re
from collections import defaultdict
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from app.db.models.gis_disease_occurrence import GISDiseaseOccurrence
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit
from app.db.models.gis_laboratory_result import GISLaboratoryResult
from app.db.models.gis_send_sample_detail import GISSendSampleDetail
from app.db.models.gis_surveillance import GISSurveillance
from app.db.models.gis_vaccination_performance import GISVaccinationPerformance


ANIMAL_POPULATION_FIELDS = {
    "گاو": ["cattle_count"],
    "گاو و گوساله": ["cattle_count"],
    "گوسفند": ["sheep_count"],
    "بز": ["goat_count"],
    "گوسفند و بز": ["sheep_count", "goat_count"],
    "دام سبک": ["sheep_count", "goat_count"],
    "بره و بزغاله": ["sheep_count", "goat_count"],
    "سگ": ["dog_count"],
    "سگ صاحبدار": ["dog_count"],
    "سگ بدون صاحب": ["dog_count"],
    "اسب": ["horse_count"],
    "تک سمی": ["horse_count"],
    "شتر": ["camel_count"],
    "گاومیش": ["buffalo_count"],
}

PUBLIC_WORDS = ("دولتی", "رایگان", "اداره", "شبکه", "عمومی")
PRIVATE_WORDS = ("خصوصی", "غیردولتی", "کلینیک", "داروخانه", "مرکز خصوصی")


def _norm(value: Any) -> str:
    return str(value or "").strip().replace("ي", "ی").replace("ك", "ک").replace("‌", " ").lower()


def _fmt(value: float | int) -> str:
    return f"{int(round(value)):,}".replace(",", "٬")


def _pct(value: float) -> str:
    return f"{value:.1f}%"


def _jalali_to_gregorian(jy: int, jm: int, jd: int) -> date:
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    days += (jm - 1) * 31 if jm < 7 else ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if days > 36524:
        gy += 100 * ((days - 1) // 36524)
        days = (days - 1) % 36524
        if days >= 365:
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        gy += (days - 1) // 365
        days = (days - 1) % 365
    gd = days + 1
    leap = (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)
    month_days = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 1
    while gd > month_days[gm - 1]:
        gd -= month_days[gm - 1]
        gm += 1
    return date(gy, gm, gd)


def _year_window(jy: int, quarter: int | None = None, month: int | None = None) -> tuple[date, date]:
    if quarter:
        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2
        end_day = 31 if end_month <= 6 else 30
        return _jalali_to_gregorian(jy, start_month, 1), _jalali_to_gregorian(jy, end_month, end_day)
    if month:
        end_day = 31 if month <= 6 else 30
        return _jalali_to_gregorian(jy, month, 1), _jalali_to_gregorian(jy, month, end_day)
    return _jalali_to_gregorian(jy, 1, 1), _jalali_to_gregorian(jy, 12, 30)


def _extract_years(text: str) -> list[int]:
    return [int(x) for x in re.findall(r"(?<!\d)(13\d{2}|14\d{2})(?!\d)", text)]


def _extract_quarter(text: str) -> int | None:
    m = re.search(r"(?:سه|3)\s*ماه(?:ه)?(?:\s*ی)?\s*(?:اول|۱|1)", text)
    if m:
        return 1
    m = re.search(r"(?:چهار|4)\s*ماه(?:ه)?(?:\s*ی)?\s*(?:اول|۱|1)", text)
    return 1 if m else None


def _extract_animal(text: str) -> str | None:
    t = _norm(text)
    for animal in sorted(ANIMAL_POPULATION_FIELDS, key=len, reverse=True):
        if _norm(animal) in t:
            return animal
    return None


def _extract_disease(text: str) -> str | None:
    candidates = ("بروسلوز", "تب برفکی", "ppr", "آبله", "شاربن", "لمپی اسکین", "هاری", "سل", "مشمشه")
    t = _norm(text)
    for item in candidates:
        if _norm(item) in t:
            return item
    return None


def _operation_segment(value: Any) -> str:
    t = _norm(value)
    if any(x in t for x in PUBLIC_WORDS):
        return "public"
    if any(x in t for x in PRIVATE_WORDS):
        return "private"
    return "other"


def _population_for_units(units: list[GISEpidemiologyUnit], animal: str | None) -> int:
    if animal:
        fields = ANIMAL_POPULATION_FIELDS.get(animal, [])
    else:
        fields = ["sheep_count", "cattle_count", "goat_count", "horse_count", "dog_count", "camel_count", "buffalo_count"]
    return sum(int(getattr(u, field, 0) or 0) for u in units for field in fields)


def _filter_text(column, value: str | None):
    if not value:
        return None
    return column.ilike(f"%{value}%")


class GISDiseaseControlAIService:
    @classmethod
    def answer(cls, db: Session, question: str, province_code: str | None = None, county_code: str | None = None) -> dict[str, Any]:
        q = _norm(question)
        years = _extract_years(q)
        quarter = _extract_quarter(q)
        animal = _extract_animal(q)
        disease = _extract_disease(q)
        wants_private = any(x in q for x in ("خصوصی", "غیردولتی"))
        wants_public = any(x in q for x in ("دولتی", "رایگان"))
        wants_compare = any(x in q for x in ("مقایسه", "نسبت به", "مشابه", "تغییر", "افزایش", "کاهش")) and len(years) >= 2

        if wants_compare and years:
            result = cls._vaccination_comparison(db, years[-2], years[-1], quarter, animal, disease, province_code, county_code)
            return result

        if any(x in q for x in ("واکسیناسیون", "واکسن", "پوشش")):
            return cls._vaccination_snapshot(db, animal, disease, wants_private, wants_public, province_code, county_code)

        if any(x in q for x in ("بیماری", "کانون", "رخداد", "شیوع")):
            return cls._disease_snapshot(db, disease, province_code, county_code)

        if any(x in q for x in ("مراقبت", "مثبت", "پایش")):
            return cls._surveillance_snapshot(db, province_code, county_code)

        if any(x in q for x in ("نمونه", "آزمایش", "لابراتوار")):
            return cls._sample_snapshot(db, province_code, county_code)

        return {
            "ok": False,
            "intent": "unknown",
            "answer": "سؤال را دریافت کردم، اما برای پاسخ عددی باید شاخص را مشخص‌تر کنید. مثلاً: «عملکرد واکسیناسیون بروسلوز گاوی در ۳ ماهه اول ۱۴۰۵ نسبت به ۱۴۰۴ چطور بوده؟» یا «پوشش واکسیناسیون تب برفکی در بخش خصوصی چقدر است؟»",
            "suggestions": [
                "عملکرد واکسیناسیون بروسلوز گاوی در ۳ ماهه اول ۱۴۰۵ نسبت به ۱۴۰۴ چطور بوده؟",
                "پوشش واکسیناسیون تب برفکی چقدر است؟",
                "عملکرد بخش خصوصی واکسیناسیون چقدر است؟",
                "کدام شهرستان‌ها در پوشش واکسیناسیون عقب هستند؟",
                "نرخ مثبت مراقبت و تعداد نمونه‌های بدون نتیجه چقدر است؟",
            ],
        }

    @classmethod
    def _base_vaccination_query(cls, db: Session, start: date, end: date, animal: str | None, disease: str | None, province_code: str | None, county_code: str | None):
        q = db.query(GISVaccinationPerformance).filter(GISVaccinationPerformance.vaccination_date >= start, GISVaccinationPerformance.vaccination_date <= end)
        if province_code:
            q = q.filter(GISVaccinationPerformance.province_code == province_code)
        if county_code:
            q = q.filter(GISVaccinationPerformance.county_code == county_code)
        if disease:
            cond = _filter_text(GISVaccinationPerformance.disease_name, disease)
            vaccine_cond = _filter_text(GISVaccinationPerformance.vaccine_type, disease)
            if cond is not None and vaccine_cond is not None:
                from sqlalchemy import or_
                q = q.filter(or_(cond, vaccine_cond))
        if animal:
            q = q.filter(_filter_text(GISVaccinationPerformance.animal_type, animal))
        return q

    @classmethod
    def _vaccination_comparison(cls, db: Session, old_year: int, new_year: int, quarter: int | None, animal: str | None, disease: str | None, province_code: str | None, county_code: str | None):
        old_start, old_end = _year_window(old_year, quarter=quarter)
        new_start, new_end = _year_window(new_year, quarter=quarter)
        rows = []
        for label, start, end, jy in (("سال قبل", old_start, old_end, old_year), ("سال جاری", new_start, new_end, new_year)):
            records = cls._base_vaccination_query(db, start, end, animal, disease, province_code, county_code).all()
            vaccinated = sum(int(r.vaccinated_animals or 0) for r in records)
            public = sum(int(r.vaccinated_animals or 0) for r in records if _operation_segment(r.operation_type) == "public")
            private = sum(int(r.vaccinated_animals or 0) for r in records if _operation_segment(r.operation_type) == "private")
            unit_ids = {r.epidemiology_unit_id for r in records if r.epidemiology_unit_id}
            units = db.query(GISEpidemiologyUnit).filter(GISEpidemiologyUnit.id.in_(unit_ids)).all() if unit_ids else []
            population = _population_for_units(units, animal)
            rows.append({"jalali_year": jy, "records": len(records), "vaccinated": vaccinated, "public": public, "private": private, "population": population, "coverage": round(vaccinated / population * 100, 2) if population else 0})
        old, new = rows[0], rows[1]
        delta = new["vaccinated"] - old["vaccinated"]
        pct_change = round(delta / old["vaccinated"] * 100, 2) if old["vaccinated"] else None
        coverage_delta = round(new["coverage"] - old["coverage"], 2)
        period_text = "۳ ماهه اول" if quarter == 1 else "بازه انتخاب‌شده"
        subject = " ".join(x for x in (disease, animal) if x) or "همه واکسیناسیون‌ها"
        direction = "افزایش" if delta > 0 else "کاهش" if delta < 0 else "بدون تغییر"
        answer = (
            f"برای {subject} در {period_text}، عملکرد ثبت‌شده از {_fmt(old['vaccinated'])} در سال {old_year} به {_fmt(new['vaccinated'])} در سال {new_year} رسیده است؛ یعنی {direction} {_fmt(abs(delta))} مورد"
            + (f" ({_pct(abs(pct_change))} نسبت به سال قبل)" if pct_change is not None else " (مبنای درصدی برای سال قبل صفر بوده است)")
            + f". پوشش محاسبه‌شده بر مبنای جمعیت واقعی واحدهای اپیدمیولوژیک از {_pct(old['coverage'])} به {_pct(new['coverage'])} رسیده و {coverage_delta:+.1f} واحد درصد تغییر کرده است."
            + f" بخش دولتی سال {new_year}: {_fmt(new['public'])} و بخش خصوصی: {_fmt(new['private'])} مورد ثبت شده است."
        )
        return {"ok": True, "intent": "vaccination_comparison", "answer": answer, "period": {"old": [old_start.isoformat(), old_end.isoformat()], "new": [new_start.isoformat(), new_end.isoformat()]}, "filters": {"animal": animal, "disease": disease}, "data": {"old": old, "new": new, "delta": delta, "percent_change": pct_change, "coverage_delta": coverage_delta}}

    @classmethod
    def _vaccination_snapshot(cls, db: Session, animal: str | None, disease: str | None, wants_private: bool, wants_public: bool, province_code: str | None, county_code: str | None):
        q = db.query(GISVaccinationPerformance)
        if province_code:
            q = q.filter(GISVaccinationPerformance.province_code == province_code)
        if county_code:
            q = q.filter(GISVaccinationPerformance.county_code == county_code)
        if disease:
            from sqlalchemy import or_
            q = q.filter(or_(_filter_text(GISVaccinationPerformance.disease_name, disease), _filter_text(GISVaccinationPerformance.vaccine_type, disease)))
        if animal:
            q = q.filter(_filter_text(GISVaccinationPerformance.animal_type, animal))
        records = q.all()
        if wants_private:
            records = [r for r in records if _operation_segment(r.operation_type) == "private"]
        elif wants_public:
            records = [r for r in records if _operation_segment(r.operation_type) == "public"]
        vaccinated = sum(int(r.vaccinated_animals or 0) for r in records)
        unit_ids = {r.epidemiology_unit_id for r in records if r.epidemiology_unit_id}
        units = db.query(GISEpidemiologyUnit).filter(GISEpidemiologyUnit.id.in_(unit_ids)).all() if unit_ids else []
        population = _population_for_units(units, animal)
        coverage = round(vaccinated / population * 100, 2) if population else 0
        segment = "بخش خصوصی" if wants_private else "بخش دولتی" if wants_public else "کل عملیات"
        answer = f"در {segment}، {_fmt(vaccinated)} مورد واکسیناسیون ثبت شده است. با استفاده از جمعیت واقعی واحدهای اپیدمیولوژیک به عنوان مخرج، شاخص نسبت عملکرد ثبت‌شده به جمعیت مبنا {_pct(coverage)} است."
        if wants_private:
            answer += " توجه: این عدد «نفوذ/عملکرد بخش خصوصی نسبت به جمعیت مبنا» است و تا زمانی که جمعیت واجد شرایط اختصاصی بخش خصوصی ثبت نشود، نباید آن را به‌عنوان پوشش اختصاصی خصوصی تفسیر کرد."
        return {"ok": True, "intent": "vaccination_snapshot", "answer": answer, "filters": {"animal": animal, "disease": disease, "segment": segment}, "data": {"vaccinated": vaccinated, "population": population, "coverage": coverage}}

    @classmethod
    def _disease_snapshot(cls, db: Session, disease: str | None, province_code: str | None, county_code: str | None):
        q = db.query(GISDiseaseOccurrence)
        if province_code: q = q.filter(GISDiseaseOccurrence.province_code == province_code)
        if county_code: q = q.filter(GISDiseaseOccurrence.county_code == county_code)
        if disease: q = q.filter(_filter_text(GISDiseaseOccurrence.disease_name, disease))
        rows = q.all()
        outbreaks = len(rows)
        infected = sum(int(r.infected_count or 0) for r in rows)
        deaths = sum(int(r.dead_count or 0) for r in rows)
        exposed = sum(int(r.exposed_count or 0) for r in rows)
        attack = round(infected / exposed * 100, 2) if exposed else 0
        cfr = round(deaths / infected * 100, 2) if infected else 0
        return {"ok": True, "intent": "disease_snapshot", "answer": f"برای {disease or 'همه بیماری‌ها'}، {outbreaks} رخداد ثبت شده؛ مبتلایان {_fmt(infected)}، تلفات {_fmt(deaths)}، نرخ حمله {_pct(attack)} و CFR برابر {_pct(cfr)} است.", "data": {"outbreaks": outbreaks, "infected": infected, "deaths": deaths, "attack_rate": attack, "case_fatality": cfr}}

    @classmethod
    def _surveillance_snapshot(cls, db: Session, province_code: str | None, county_code: str | None):
        q = db.query(GISSurveillance)
        if province_code: q = q.filter(GISSurveillance.province_code == province_code)
        if county_code: q = q.filter(GISSurveillance.county_code == county_code)
        rows = q.all()
        examined = sum(int(r.total_animals or 0) for r in rows)
        positive = sum(int(r.positive or 0) for r in rows)
        suspected = sum(int(r.suspected or 0) for r in rows)
        rate = round(positive / examined * 100, 2) if examined else 0
        return {"ok": True, "intent": "surveillance_snapshot", "answer": f"در داده‌های مراقبت، {_fmt(examined)} رأس/مورد بررسی شده، {_fmt(positive)} مورد مثبت و {_fmt(suspected)} مورد مشکوک ثبت شده است. نرخ مثبت {_pct(rate)} است.", "data": {"examined": examined, "positive": positive, "suspected": suspected, "positive_rate": rate}}

    @classmethod
    def _sample_snapshot(cls, db: Session, province_code: str | None, county_code: str | None):
        q = db.query(GISSendSampleDetail)
        if province_code: q = q.filter(GISSendSampleDetail.province_code == province_code)
        if county_code: q = q.filter(GISSendSampleDetail.county_code == county_code)
        rows = q.all()
        samples = sum(int(r.sample_count or 0) for r in rows)
        without = sum(1 for r in rows if not r.result_status)
        lq = db.query(GISLaboratoryResult)
        if province_code: lq = lq.filter(GISLaboratoryResult.province_code == province_code)
        if county_code: lq = lq.filter(GISLaboratoryResult.county_code == county_code)
        lab = lq.all()
        lab_samples = sum(int(r.sample_count or 0) for r in lab)
        return {"ok": True, "intent": "sample_snapshot", "answer": f"تعداد نمونه‌های ثبت‌شده {_fmt(samples)}، موارد بدون نتیجه {_fmt(without)} و تعداد نمونه‌های ثبت‌شده در نتایج آزمایشگاهی {_fmt(lab_samples)} است.", "data": {"samples": samples, "without_result": without, "laboratory_samples": lab_samples}}
