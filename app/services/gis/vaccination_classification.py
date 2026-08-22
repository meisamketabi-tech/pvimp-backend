from __future__ import annotations

"""Semantic classification for real GIS vaccination-performance records.

Raw GIS values are preserved. This module supplies the canonical semantic
layer used by KPI/reporting code.
"""

from dataclasses import dataclass
import re

VACCINATION_ACTIVITY = "VACCINATION"
SURVEILLANCE_ACTIVITY = "SURVEILLANCE"
OTHER_ACTIVITY = "OTHER"

ANIMAL_LIGHT = "LIGHT_LIVESTOCK"
ANIMAL_HEAVY = "HEAVY_LIVESTOCK"
ANIMAL_EQUINE = "EQUINE"
ANIMAL_DOG = "DOG"
ANIMAL_CAT = "CAT"
ANIMAL_CAMEL = "CAMEL"
ANIMAL_UNKNOWN = "UNKNOWN"
ANIMAL_MIXED = "MIXED"


@dataclass(frozen=True)
class VaccinationClassification:
    raw_name: str
    standard_name: str
    disease_name: str | None
    activity_type: str


def _clean(value: str | None) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    value = value.replace("ي", "ی").replace("ى", "ی").replace("ك", "ک")
    value = value.replace("ـ", "")
    value = re.sub(r"[\u200c\u200d]+", "‌", value)
    value = re.sub(r"\s+", " ", value)
    return value


def _compact(value: str) -> str:
    return value.replace(" ", "").replace("‌", "").replace("-", "")


# Exact real values observed in gis_vaccination_performances.
_VACCINE_ALIASES: dict[str, VaccinationClassification] = {
    "آبله": VaccinationClassification("", "آبله", "آبله", VACCINATION_ACTIVITY),
    "بروسلوز دام سبک": VaccinationClassification("", "بروسلوز دام سبک", "بروسلوز", VACCINATION_ACTIVITY),
    "بروسلوز گاو و گوساله": VaccinationClassification("", "بروسلوز گاو و گوساله", "بروسلوز", VACCINATION_ACTIVITY),
    "تب برفکی": VaccinationClassification("", "تب برفکی", "تب برفکی", VACCINATION_ACTIVITY),
    "تب برفکی هگزا": VaccinationClassification("", "تب برفکی هگزا", "تب برفکی", VACCINATION_ACTIVITY),
    "چهارگانه کلستریدیایی": VaccinationClassification("", "چهارگانه کلستریدیایی", "کلستریدیوز", VACCINATION_ACTIVITY),
    "شاربن": VaccinationClassification("", "شاربن", "شاربن", VACCINATION_ACTIVITY),
    "کزاز": VaccinationClassification("", "کزاز", "کزاز", VACCINATION_ACTIVITY),
    "هاری": VaccinationClassification("", "هاری", "هاری", VACCINATION_ACTIVITY),
    "هپاتیت نکروزان": VaccinationClassification("", "هپاتیت نکروزان", "هپاتیت نکروزان", VACCINATION_ACTIVITY),
    "آگالاکسی": VaccinationClassification("", "آگالاکسی", "آگالاکسی", VACCINATION_ACTIVITY),
    "اگالاکسی": VaccinationClassification("", "اگالاکسی", "اگالاکسی", VACCINATION_ACTIVITY),
    "اکتیما": VaccinationClassification("", "اکتیما", "اکتیما", VACCINATION_ACTIVITY),
    "سموم": VaccinationClassification("", "سموم", None, OTHER_ACTIVITY),
    "تست سل": VaccinationClassification("", "تست سل", "سل", SURVEILLANCE_ACTIVITY),
    "واکسن های سگ": VaccinationClassification("", "واکسن های سگ", None, VACCINATION_ACTIVITY),
    "واکسن های گربه": VaccinationClassification("", "واکسن های گربه", None, VACCINATION_ACTIVITY),
    "پلی والان(چندگانه) - (غیرفعال)": VaccinationClassification("", "پلی‌والان چندگانه غیرفعال", None, VACCINATION_ACTIVITY),
    "پلی والان(چندگانه) - (غیرفعال) آنتریت پارواویروسی سگ , بیماری تنفسی عفونی سگ (تراکئوبرونشیت عفونی) , دیستمپر , لپتوسپیروز , هاری , هپاتیت عفونی سگ": VaccinationClassification("", "پلی‌والان چندگانه سگ", "بیماری‌های چندگانه سگ", VACCINATION_ACTIVITY),
    "دوگانه آنتریت پارواویروسی سگ , دیستمپر": VaccinationClassification("", "دوگانه آنتریت پارواویروسی سگ و دیستمپر", "آنتریت پارواویروسی سگ/دیستمپر", VACCINATION_ACTIVITY),
    "دوگانه کورینه باکتریوم+سالمونلوز": VaccinationClassification("", "دوگانه کورینه باکتریوم + سالمونلوز", "کورینه باکتریوم/سالمونلوز", VACCINATION_ACTIVITY),
    "سه گانه آنتروتوکسمی، شاربن علامتی، کزاز": VaccinationClassification("", "سه‌گانه آنتروتوکسمی + شاربن علامتی + کزاز", "آنتروتوکسمی/شاربن/کزاز", VACCINATION_ACTIVITY),
}


def classify_vaccine(raw_name: str | None) -> VaccinationClassification:
    raw = _clean(raw_name)
    if raw in _VACCINE_ALIASES:
        rule = _VACCINE_ALIASES[raw]
        return VaccinationClassification(raw, rule.standard_name, rule.disease_name, rule.activity_type)

    compact = _compact(raw)
    if compact.startswith("لمپیاسکین") or compact.startswith("لامپیاسکین"):
        return VaccinationClassification(raw, "لمپی‌اسکین", "لمپی‌اسکین", VACCINATION_ACTIVITY)
    if compact.startswith("طاعوننشخوارکنندگانکوچک") or compact in {"ppr", "pp r".replace(" ", "")}:
        return VaccinationClassification(raw, "طاعون نشخوارکنندگان کوچک", "PPR", VACCINATION_ACTIVITY)
    if compact.startswith("دوگانهآنتریت"):
        return VaccinationClassification(raw, "دوگانه آنتریت", "آنتریت", VACCINATION_ACTIVITY)
    if compact.startswith("دوگانهکورینه"):
        return VaccinationClassification(raw, "دوگانه کورینه", "کورینه/باکتریوم", VACCINATION_ACTIVITY)
    if compact.startswith("سهگانهآنتروتوکسمی"):
        return VaccinationClassification(raw, "سه‌گانه آنتروتوکسمی + شاربن + کزاز", "آنتروتوکسمی/شاربن/کزاز", VACCINATION_ACTIVITY)
    if compact.startswith("آکتیما"):
        return VaccinationClassification(raw, "اکتیما", "اکتیما", VACCINATION_ACTIVITY)

    return VaccinationClassification(raw, raw or "نامشخص", raw or None, OTHER_ACTIVITY)


_ANIMAL_ALIASES: dict[str, tuple[str, str]] = {
    "گوسفند": ("گوسفند", ANIMAL_LIGHT),
    "بز": ("بز", ANIMAL_LIGHT),
    "بره": ("بره", ANIMAL_LIGHT),
    "بزغاله": ("بزغاله", ANIMAL_LIGHT),
    "گاو": ("گاو", ANIMAL_HEAVY),
    "گوساله": ("گوساله", ANIMAL_HEAVY),
    "گاومیش": ("گاومیش", ANIMAL_HEAVY),
    "گاو میش": ("گاومیش", ANIMAL_HEAVY),
    "اسب": ("اسب", ANIMAL_EQUINE),
    "الاغ": ("الاغ", ANIMAL_EQUINE),
    "قاطر": ("قاطر", ANIMAL_EQUINE),
    "سگ": ("سگ", ANIMAL_DOG),
    "سگ صاحبدار": ("سگ صاحبدار", ANIMAL_DOG),
    "سگ بدون صاحب": ("سگ بدون صاحب", ANIMAL_DOG),
    "گربه": ("گربه", ANIMAL_CAT),
    "شتر": ("شتر", ANIMAL_CAMEL),
}


def classify_animal(raw_name: str | None) -> dict[str, object]:
    raw = _clean(raw_name)
    if raw in _ANIMAL_ALIASES:
        standard_name, group = _ANIMAL_ALIASES[raw]
        return {"raw_animal_type": raw, "standard_animal_type": standard_name, "animal_group": group, "is_composite": False}

    parts = [p.strip() for p in re.split(r"\s+و\s+", raw) if p.strip()]
    if len(parts) > 1 and all(part in _ANIMAL_ALIASES for part in parts):
        groups = {_ANIMAL_ALIASES[part][1] for part in parts}
        return {
            "raw_animal_type": raw,
            "standard_animal_type": " و ".join(_ANIMAL_ALIASES[part][0] for part in parts),
            "animal_group": next(iter(groups)) if len(groups) == 1 else ANIMAL_MIXED,
            "is_composite": True,
        }

    return {"raw_animal_type": raw, "standard_animal_type": raw or "نامشخص", "animal_group": ANIMAL_UNKNOWN, "is_composite": False}


def is_kpi_vaccination(raw_name: str | None) -> bool:
    return classify_vaccine(raw_name).activity_type == VACCINATION_ACTIVITY


def standard_vaccine_name(raw_name: str | None) -> str:
    return classify_vaccine(raw_name).standard_name
