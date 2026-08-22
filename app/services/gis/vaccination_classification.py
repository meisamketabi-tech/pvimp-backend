from __future__ import annotations

"""Centralized classification rules for GIS vaccination KPI data.

Raw GIS values are intentionally preserved in the database. This module is the
semantic layer used by KPI/reporting code so that spelling variants, disease
aliases, activity type, and animal groups do not leak into KPI calculations.
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


@dataclass(frozen=True)
class VaccinationClassification:
    raw_name: str
    standard_name: str
    disease_name: str | None
    activity_type: str


# Ordered: more specific aliases/patterns first.
_VACCINE_RULES: tuple[tuple[re.Pattern[str], VaccinationClassification], ...] = (
    (
        re.compile(r"^لمپی\s*[-‌ ]?\s*اسکین$|^لامپی\s*[-‌ ]?\s*اسکین$"),
        VaccinationClassification("", "لمپی‌اسکین", "لمپی‌اسکین", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^لمپی\s*[-‌ ]?\s*اسکین.*"),
        VaccinationClassification("", "لمپی‌اسکین", "لمپی‌اسکین", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^لامپی\s*[-‌ ]?\s*اسکین.*"),
        VaccinationClassification("", "لمپی‌اسکین", "لمپی‌اسکین", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^تست\s*سل$"),
        VaccinationClassification("", "تست سل", "سل", SURVEILLANCE_ACTIVITY),
    ),
    (
        re.compile(r"^آبله\s*گوسفندی$"),
        VaccinationClassification("", "آبله گوسفندی", "آبله گوسفندی", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^آبله$"),
        VaccinationClassification("", "آبله", "آبله", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^بروسلوز\s*دام\s*سبک$"),
        VaccinationClassification("", "بروسلوز دام سبک", "بروسلوز", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^بروسلوز\s*گاو\s*و\s*گوساله$"),
        VaccinationClassification("", "بروسلوز گاو و گوساله", "بروسلوز", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^تب\s*برفکی\s*هگزازا$"),
        VaccinationClassification("", "تب برفکی هگزازا", "تب برفکی", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^تب\s*برفکی$"),
        VaccinationClassification("", "تب برفکی", "تب برفکی", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^چهارگانه\s*کلستریدیایی$"),
        VaccinationClassification("", "چهارگانه کلستریدیایی", "کلستریدیوز", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^دوگانه\s*آنتریت.*$"),
        VaccinationClassification("", "دوگانه آنتریت", "آنتریت", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^دوگانه\s*کورینه.*$"),
        VaccinationClassification("", "دوگانه کورینه", "کورینه/باکتریوم", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^سه‌گانه\s*آنتروتوکسمی.*$|^سه گانه\s*آنتروتوکسمی.*$"),
        VaccinationClassification("", "سه‌گانه آنتروتوکسمی + شاربن + کزاز", "آنتروتوکسمی/شاربن/کزاز", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^شاربن$"),
        VaccinationClassification("", "شاربن", "شاربن", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^طاعون\s*نشخوارکنندگان\s*کوچک$|^P\.?P\.?R$"),
        VaccinationClassification("", "طاعون نشخوارکنندگان کوچک", "PPR", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^کزاز$"),
        VaccinationClassification("", "کزاز", "کزاز", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^هاری$|^واکسن\s*هاری\s*سگ$|^واکسن\s*هاری\s*گربه$"),
        VaccinationClassification("", "هاری", "هاری", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^هپاتیت\s*نکرورزان$"),
        VaccinationClassification("", "هپاتیت نکرورزان", "هپاتیت نکرورزان", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^آکتیم.*$"),
        VaccinationClassification("", "آکتیمـا", "آکتیمـا", VACCINATION_ACTIVITY),
    ),
    (
        re.compile(r"^سموم$"),
        VaccinationClassification("", "سموم", None, OTHER_ACTIVITY),
    ),
)


def _clean(value: str | None) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    value = value.replace("ي", "ی").replace("ك", "ک")
    value = value.replace("ـ", "")
    value = re.sub(r"\s+", " ", value)
    return value


def classify_vaccine(raw_name: str | None) -> VaccinationClassification:
    raw = _clean(raw_name)
    for pattern, rule in _VACCINE_RULES:
        if pattern.fullmatch(raw):
            return VaccinationClassification(
                raw_name=raw,
                standard_name=rule.standard_name,
                disease_name=rule.disease_name,
                activity_type=rule.activity_type,
            )

    return VaccinationClassification(
        raw_name=raw,
        standard_name=raw or "نامشخص",
        disease_name=raw or None,
        activity_type=OTHER_ACTIVITY,
    )


_ANIMAL_ALIASES: dict[str, tuple[str, str]] = {
    "گوسفند": ("گوسفند", ANIMAL_LIGHT),
    "بز": ("بز", ANIMAL_LIGHT),
    "بره": ("بره", ANIMAL_LIGHT),
    "بزغاله": ("بزغاله", ANIMAL_LIGHT),
    "گاو": ("گاو", ANIMAL_HEAVY),
    "گوساله": ("گوساله", ANIMAL_HEAVY),
    "گاو میش": ("گاومیش", ANIMAL_HEAVY),
    "گاومیش": ("گاومیش", ANIMAL_HEAVY),
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
        return {
            "raw_animal_type": raw,
            "standard_animal_type": standard_name,
            "animal_group": group,
            "is_composite": False,
        }

    parts = [p.strip() for p in re.split(r"\s+و\s+", raw) if p.strip()]
    if len(parts) > 1 and all(part in _ANIMAL_ALIASES for part in parts):
        groups = { _ANIMAL_ALIASES[part][1] for part in parts }
        return {
            "raw_animal_type": raw,
            "standard_animal_type": " و ".join(_ANIMAL_ALIASES[part][0] for part in parts),
            "animal_group": next(iter(groups)) if len(groups) == 1 else "MIXED",
            "is_composite": True,
        }

    return {
        "raw_animal_type": raw,
        "standard_animal_type": raw or "نامشخص",
        "animal_group": ANIMAL_UNKNOWN,
        "is_composite": False,
    }


def is_kpi_vaccination(raw_name: str | None) -> bool:
    return classify_vaccine(raw_name).activity_type == VACCINATION_ACTIVITY


def standard_vaccine_name(raw_name: str | None) -> str:
    return classify_vaccine(raw_name).standard_name
