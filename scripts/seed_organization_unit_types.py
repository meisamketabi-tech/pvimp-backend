from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.organization_unit_type import OrganizationUnitType


def seed():

    db: Session = SessionLocal()

    data = [
        {
            "code": "GENERAL_DIRECTORATE",
            "name": "اداره کل دامپزشکی استان زنجان",
            "level_order": 1,
        },
        {
            "code": "DEPUTY",
            "name": "معاونت",
            "level_order": 2,
        },
        {
            "code": "MANAGEMENT",
            "name": "مدیریت",
            "level_order": 3,
        },
        {
            "code": "DEPARTMENT",
            "name": "اداره",
            "level_order": 4,
        },
        {
            "code": "UNIT",
            "name": "واحد",
            "level_order": 5,
        },
        {
            "code": "COUNTY_OFFICE",
            "name": "اداره دامپزشکی شهرستان",
            "level_order": 6,
        },
        {
            "code": "INSPECTION_POST",
            "name": "پست قرنطینه و بازرسی",
            "level_order": 7,
        },
    ]


    try:

        for item in data:

            exists = (
                db.query(OrganizationUnitType)
                .filter(
                    OrganizationUnitType.code == item["code"]
                )
                .first()
            )

            if not exists:
                db.add(
                    OrganizationUnitType(**item)
                )

        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed()
