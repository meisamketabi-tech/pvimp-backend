from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit
from app.db.models.organization_responsibility import OrganizationResponsibility


def seed():

    db = SessionLocal()

    try:

        data = [

            {
                "unit": "ANIMAL_HEALTH_DEPARTMENT",
                "title": "پایش و کنترل بیماری‌های دامی",
                "description": "مراقبت، پیشگیری و کنترل بیماری‌های دامی",
                "inspection": 14,
            },

            {
                "unit": "POULTRY_DEPARTMENT",
                "title": "پایش و کنترل بیماری‌های طیور، زنبور عسل، کرم ابریشم و آبزیان",
                "description": "مراقبت و کنترل بیماری‌های جمعیت‌های هدف",
                "inspection": 15,
            },

            {
                "unit": "PUBLIC_HEALTH_DEPARTMENT",
                "title": "نظارت بر بهداشت عمومی و مواد غذایی",
                "description": "بازرسی مراکز تولید، عرضه و فرآورده‌های خام دامی",
                "inspection": 16,
            },

            {
                "unit": "QUARANTINE_UNIT",
                "title": "کنترل قرنطینه و امنیت زیستی",
                "description": "نظارت بر جابجایی دام، فرآورده‌ها و الزامات امنیت زیستی",
                "inspection": 17,
            },

            {
                "unit": "DIAGNOSIS_DEPARTMENT",
                "title": "نظارت بر خدمات تشخیص و درمان",
                "description": "نظارت بر فعالیت مراکز تشخیص و درمان دامپزشکی",
                "inspection": 18,
            },

        ]


        for item in data:

            unit = (
                db.query(OrganizationUnit)
                .filter(
                    OrganizationUnit.code == item["unit"]
                )
                .first()
            )


            if not unit:
                continue


            exists = (
                db.query(OrganizationResponsibility)
                .filter(
                    OrganizationResponsibility.organization_unit_id == unit.id,
                    OrganizationResponsibility.title == item["title"]
                )
                .first()
            )


            if not exists:

                db.add(
                    OrganizationResponsibility(
                        organization_unit_id=unit.id,
                        inspection_type_id=item["inspection"],
                        title=item["title"],
                        description=item["description"],
                        priority=1,
                        is_active=True,
                    )
                )


        db.commit()

        print("Organization responsibilities seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()