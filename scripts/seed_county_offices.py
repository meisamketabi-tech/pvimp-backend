from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit


def seed():

    db = SessionLocal()

    try:

        root = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.code ==
                "ZANJAN_VETERINARY_GENERAL_DIRECTORATE"
            )
            .first()
        )


        counties = [

            {
                "code": "ZANJAN_COUNTY_VET",
                "name": "اداره دامپزشکی شهرستان زنجان",
            },

            {
                "code": "ABHAR_COUNTY_VET",
                "name": "اداره دامپزشکی شهرستان ابهر",
            },

            {
                "code": "KHORAMDAREH_COUNTY_VET",
                "name": "اداره دامپزشکی شهرستان خرمدره",
            },

            {
                "code": "KHODABANDEH_COUNTY_VET",
                "name": "اداره دامپزشکی شهرستان خدابنده",
            },

            {
                "code": "TAROM_COUNTY_VET",
                "name": "اداره دامپزشکی شهرستان طارم",
            },

            {
                "code": "MAH NESHAN_COUNTY_VET",
                "name": "اداره دامپزشکی شهرستان ماهنشان",
            },

            {
                "code": "IJROOD_COUNTY_VET",
                "name": "اداره دامپزشکی شهرستان ایجرود",
            },

            {
                "code": "SOLTANIYEH_COUNTY_VET",
                "name": "اداره دامپزشکی شهرستان سلطانیه",
            },

        ]


        for item in counties:

            exists = (
                db.query(OrganizationUnit)
                .filter(
                    OrganizationUnit.code == item["code"]
                )
                .first()
            )


            if not exists:

                unit = OrganizationUnit(
                    code=item["code"],
                    name=item["name"],
                    unit_type="COUNTY_OFFICE",
                    parent_id=root.id,
                )

                db.add(unit)


        db.commit()

        print("County veterinary offices seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()

