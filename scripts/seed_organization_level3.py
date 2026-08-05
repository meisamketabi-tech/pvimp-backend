from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit


def seed():

    db = SessionLocal()

    try:

        parents = {

            "HEALTH_DEPUTY":
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.code=="HEALTH_DEPUTY"
            )
            .first(),


            "DEVELOPMENT_DEPUTY":
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.code=="DEVELOPMENT_DEPUTY"
            )
            .first(),

        }


        units = [

            {
                "code": "ANIMAL_HEALTH_DEPARTMENT",
                "name": "اداره بهداشت و مدیریت بیماری‌های دامی",
                "parent": "HEALTH_DEPUTY",
            },

            {
                "code": "POULTRY_HEALTH_DEPARTMENT",
                "name": "اداره بهداشت و مدیریت بیماری‌های طیور",
                "parent": "HEALTH_DEPUTY",
            },

            {
                "code": "PUBLIC_HEALTH_DEPARTMENT",
                "name": "اداره نظارت بر بهداشت عمومی و مواد غذایی",
                "parent": "HEALTH_DEPUTY",
            },

	    {
                "code": "DIAGNOSIS_TREATMENT",
                "name": "اداره تشخیص و درمان",
                                 "parent": "HEALTH_DEPUTY",
            },
            {
                "code": "QUARANTINE_DEPARTMENT",
                "name": "اداره قرنطینه و امنیت زیستی",
                "parent": "HEALTH_DEPUTY",
            },


            {
                "code": "ADMIN_DEPARTMENT",
                "name": "اداره امور اداری",
                "parent": "DEVELOPMENT_DEPUTY",
            },

            {
                "code": "FINANCE_DEPARTMENT",
                "name": "اداره امور مالی",
                "parent": "DEVELOPMENT_DEPUTY",
            },

            {
                "code": "IT_DEPARTMENT",
                "name": "اداره فناوری اطلاعات",
                "parent": "DEVELOPMENT_DEPUTY",
            },

        ]


        for item in units:

            exists = (
                db.query(OrganizationUnit)
                .filter(
                    OrganizationUnit.code == item["code"]
                )
                .first()
            )


            if not exists:

                parent = parents[item["parent"]]

                unit = OrganizationUnit(
                    code=item["code"],
                    name=item["name"],
                    unit_type="DEPARTMENT",
                    parent_id=parent.id,
                )

                db.add(unit)


        db.commit()

        print("Organization level 3 seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()

