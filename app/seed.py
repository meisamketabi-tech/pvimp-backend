from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal

from app.db.models.user import User
from app.db.models.gis_epidemiology_unit_type import GISEpidemiologyUnitType
from app.db.models.gis_province import GISProvince
from app.db.models.gis_epidemiology_unit import GISEpidemiologyUnit


def seed_admin(db: Session):

    user = db.query(User).filter(User.username == "admin").first()

    if user:
        user.password_hash = get_password_hash("Admin@12345")
        user.is_active = True
        db.commit()
        print("Admin password reset completed")
        return

    user = User(
        username="admin",
        full_name="System Admin",
        email="admin@example.com",
        mobile=None,
        is_active=True,
        password_hash=get_password_hash("Admin@12345"),
    )

    db.add(user)
    db.commit()

    print("Admin user created")


def seed_gis_unit_types(db: Session):

    types = [
        {
            "title": "Province",
            "code": "PROVINCE",
            "description": "Provincial epidemiology unit",
        },
        {
            "title": "County",
            "code": "COUNTY",
            "description": "County epidemiology unit",
        },
        {
            "title": "Village",
            "code": "VILLAGE",
            "description": "Village epidemiology unit",
        },
        {
            "title": "Farm",
            "code": "FARM",
            "description": "Animal farm epidemiology unit",
        },
    ]

    for item in types:
        exists = (
            db.query(GISEpidemiologyUnitType)
            .filter(GISEpidemiologyUnitType.code == item["code"])
            .first()
        )

        if not exists:
            db.add(GISEpidemiologyUnitType(**item))

    db.commit()
    print("GIS unit types seeded")


def seed_gis_provinces(db: Session):

    provinces = [
        {
            "province_code": "THR",
            "province_name": "Tehran",
        },
        {
            "province_code": "ISF",
            "province_name": "Isfahan",
        },
        {
            "province_code": "FRS",
            "province_name": "Fars",
        },
    ]

    for item in provinces:
        exists = (
            db.query(GISProvince)
            .filter(GISProvince.province_code == item["province_code"])
            .first()
        )

        if not exists:
            db.add(GISProvince(**item))

    db.commit()
    print("GIS provinces seeded")


def seed_gis_units(db: Session):

    province = db.query(GISProvince).filter(GISProvince.province_code == "THR").first()

    farm_type = (
        db.query(GISEpidemiologyUnitType)
        .filter(GISEpidemiologyUnitType.code == "FARM")
        .first()
    )

    if not province or not farm_type:
        return

    exists = (
        db.query(GISEpidemiologyUnit)
        .filter(GISEpidemiologyUnit.unit_code == "THR-FARM-001")
        .first()
    )

    if not exists:

        unit = GISEpidemiologyUnit(
            unit_name="Sample Dairy Farm",
            unit_code="THR-FARM-001",
            unit_type_id=farm_type.id,
            province_id=province.id,
            latitude=35.6892,
            longitude=51.3890,
            user_name="Farmer",
            sheep_count=50,
            cattle_count=120,
            goat_count=10,
            is_active=True,
        )

        db.add(unit)
        db.commit()

    print("GIS units seeded")


def seed(db: Session):

    seed_admin(db)
    seed_gis_unit_types(db)
    seed_gis_provinces(db)
    seed_gis_units(db)


if __name__ == "__main__":

    db = SessionLocal()

    try:
        seed(db)

    finally:
        db.close()
