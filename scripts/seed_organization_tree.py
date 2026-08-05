from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit
from app.db.models.assignment import UserAssignment
from app.db.models.organization_unit_position import OrganizationUnitPosition
from app.db.models.organization_responsibility import OrganizationResponsibility


db = SessionLocal()

from sqlalchemy import text


# ---------------------------------------------
# پاکسازی ساختار قبلی
# ---------------------------------------------

db.execute(text("""
TRUNCATE TABLE
    inspections,
    user_assignments,
    organization_unit_positions,
    organization_responsibilities,
    organization_unit_areas,
    organization_units
RESTART IDENTITY CASCADE
"""))

db.commit()

def add(name, code, unit_type, parent=None):

    obj = OrganizationUnit(
        name=name,
        code=code,
        unit_type=unit_type,
        parent_id=parent.id if parent else None,
        is_active=True,
    )

    db.add(obj)
    db.flush()

    return obj


# ======================================================
# اداره کل
# ======================================================

general = add(
    "اداره کل دامپزشکی استان زنجان",
    "GENERAL_DIRECTORATE",
    "GENERAL_DIRECTORATE",
)


# ======================================================
# حوزه مدیریت
# ======================================================

management = add(
    "حوزه مدیریت",
    "MANAGEMENT",
    "MANAGEMENT",
    general,
)

add("دفتر مدیرکل", "DIRECTOR_OFFICE", "UNIT", management)
add("نماینده ولی فقیه", "RELIGIOUS_REPRESENTATIVE", "UNIT", management)
add("حراست", "SECURITY", "UNIT", management)
add("امور حقوقی", "LEGAL", "UNIT", management)
add("روابط عمومی", "PUBLIC_RELATIONS", "UNIT", management)
add("پدافند غیرعامل و مدیریت بحران", "CRISIS", "UNIT", management)


# ======================================================
# معاونت سلامت
# ======================================================

health = add(
    "معاونت سلامت",
    "HEALTH_DEPUTY",
    "DEPUTY",
    general,
)

add(
    "اداره بهداشت و مدیریت بیماری های دامی",
    "ANIMAL_HEALTH_DEPARTMENT",
    "DEPARTMENT",
    health,
)

add(
    "واحد قرنطینه و امنیت زیستی",
    "QUARANTINE_UNIT",
    "UNIT",
    health,
)

add(
    "اداره بهداشت و مدیریت بیماری های طیور ، زنبور عسل، کرم ابریشم و آبزیان",
    "POULTRY_DEPARTMENT",
    "DEPARTMENT",
    health,
)

add(
    "اداره نظارت بر بهداشت عمومی و مواد غذایی",
    "PUBLIC_HEALTH_DEPARTMENT",
    "DEPARTMENT",
    health,
)

add(
    "اداره تشخیص و درمان",
    "DIAGNOSIS_DEPARTMENT",
    "DEPARTMENT",
    health,
)


# ======================================================
# معاونت توسعه
# ======================================================

resource = add(
    "معاونت توسعه و مدیریت منابع",
    "RESOURCE_DEPUTY",
    "DEPUTY",
    general,
)

add(
    "اداره امور پشتیبانی و رفاه",
    "SUPPORT_DEPARTMENT",
    "DEPARTMENT",
    resource,
)

add(
    "اداره امور مالی",
    "FINANCE_DEPARTMENT",
    "DEPARTMENT",
    resource,
)

add(
    "اداره فن آوری اطلاعات ، ارتباطات و تحول اداری",
    "IT_DEPARTMENT",
    "DEPARTMENT",
    resource,
)

add(
    "اداره طرح برنامه و بودجه",
    "PLAN_BUDGET_DEPARTMENT",
    "DEPARTMENT",
    resource,
)


# ======================================================
# ادارات شهرستان
# ======================================================

counties_root = add(
    "ادارات شهرستان",
    "COUNTIES",
    "COUNTIES",
    general,
)

counties = [
    "ابهر",
    "ایجرود",
    "طارم",
    "زنجان",
    "خرمدره",
    "خدابنده",
    "سلطانیه",
    "ماهنشان",
]

for county in counties:

    office = add(
        f"اداره دامپزشکی شهرستان {county}",
        f"COUNTY_{county}",
        "COUNTY_OFFICE",
        counties_root,
    )

    add(
        f"رئیس اداره دامپزشکی شهرستان {county}",
        f"HEAD_{county}",
        "UNIT",
        office,
    )

    add(
        "کارشناس بررسی، مبارزه و مراقبت بیماری‌های دامی",
        f"ANIMAL_{county}",
        "UNIT",
        office,
    )

    add(
        "کارشناس بررسی، مبارزه و مراقبت بیماری‌های طیور",
        f"POULTRY_{county}",
        "UNIT",
        office,
    )

    add(
        "کارشناس امور قرنطینه و امنیت زیستی",
        f"QUARANTINE_{county}",
        "UNIT",
        office,
    )

    add(
        "کارشناس نظارت بر بهداشت کشتارگاه‌ها",
        f"SLAUGHTER_{county}",
        "UNIT",
        office,
    )

    add(
        "کارشناس تشخیص و درمان",
        f"DIAGNOSIS_{county}",
        "UNIT",
        office,
    )

    add(
        "کارشناس امور مالی",
        f"FINANCE_{county}",
        "UNIT",
        office,
    )


db.commit()
db.close()

print("Organization tree recreated successfully.")