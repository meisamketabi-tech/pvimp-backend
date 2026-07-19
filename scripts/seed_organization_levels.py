from app.db.session import SessionLocal
from app.db.models.organization_level import OrganizationLevel


def seed():

    db = SessionLocal()

    data = [
        {
            "code": "GENERAL_DIRECTORATE",
            "name": "اداره کل دامپزشکی استان",
            "level_order": 1,
            "description": "سطح اصلی اداره کل"
        },
        {
            "code": "DEPUTY",
            "name": "معاونت",
            "level_order": 2,
            "description": "معاونت‌های اداره کل"
        },
        {
            "code": "DEPARTMENT",
            "name": "اداره",
            "level_order": 3,
            "description": "ادارات تخصصی"
        },
        {
            "code": "UNIT",
            "name": "واحد",
            "level_order": 4,
            "description": "واحدهای داخلی"
        },
        {
            "code": "COUNTY",
            "name": "اداره دامپزشکی شهرستان",
            "level_order": 5,
            "description": "واحدهای شهرستانی"
        }
    ]


    try:

        for item in data:

            exists = (
                db.query(OrganizationLevel)
                .filter(
                    OrganizationLevel.code == item["code"]
                )
                .first()
            )

            if not exists:
                db.add(
                    OrganizationLevel(**item)
                )


        db.commit()

        print("Organization levels seeded")


    finally:
        db.close()


if __name__ == "__main__":
    seed()
