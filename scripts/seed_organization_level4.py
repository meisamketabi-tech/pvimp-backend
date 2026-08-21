from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit


def seed():

    db = SessionLocal()

    try:

        parents = {}

        parent_codes = [

            "ANIMAL_HEALTH_DEPARTMENT",
            "POULTRY_HEALTH_DEPARTMENT",
            "PUBLIC_HEALTH_DEPARTMENT",
	    "DIAGNOSIS_TREATMENT",
            "QUARANTINE_DEPARTMENT",
            "ADMIN_DEPARTMENT",
            "FINANCE_DEPARTMENT",
            "IT_DEPARTMENT",

        ]


        for code in parent_codes:

            parents[code] = (
                db.query(OrganizationUnit)
                .filter(
                    OrganizationUnit.code == code
                )
                .first()
            )


        units = [

            {
                "code":"ANIMAL_DISEASE_UNIT",
                "name":"واحد بیماری‌های دامی",
                "parent":"ANIMAL_HEALTH_DEPARTMENT"
            },

            {
                "code":"ANIMAL_CONTROL_UNIT",
                "name":"واحد مبارزه و پیشگیری",
                "parent":"ANIMAL_HEALTH_DEPARTMENT"
            },

            {
                "code":"VACCINATION_UNIT",
                "name":"واحد واکسیناسیون",
                "parent":"ANIMAL_HEALTH_DEPARTMENT"
            },


            {
                "code":"POULTRY_DISEASE_UNIT",
                "name":"واحد بیماری‌های طیور",
                "parent":"POULTRY_HEALTH_DEPARTMENT"
            },

            {
                "code":"POULTRY_SURVEILLANCE_UNIT",
                "name":"واحد مراقبت طیور",
                "parent":"POULTRY_HEALTH_DEPARTMENT"
            },


            {
                "code":"SLAUGHTERHOUSE_SUPERVISION_UNIT",
                "name":"واحد نظارت بر کشتارگاه‌ها",
                "parent":"PUBLIC_HEALTH_DEPARTMENT"
            },

            {
                "code":"DISTRIBUTION_SUPERVISION_UNIT",
                "name":"واحد نظارت بر مراکز عرضه",
                "parent":"PUBLIC_HEALTH_DEPARTMENT"
            },

            {
                "code":"RAW_MATERIAL_UNIT",
                "name":"واحد مواد خام دامی",
                "parent":"PUBLIC_HEALTH_DEPARTMENT"
            },


            {
                "code":"BORDER_QUARANTINE_UNIT",
                "name":"واحد قرنطینه مرزی",
                "parent":"QUARANTINE_DEPARTMENT"
            },

	    {
	        "code":"LABORATORY",
	        "name":"آزمایشگاه",
 	          "parent":"DIAGNOSIS_TREATMENT"
	    },

            {
                "code":"TRANSPORT_QUARANTINE_UNIT",
                "name":"واحد حمل و نقل دام و فرآورده",
                "parent":"QUARANTINE_DEPARTMENT"
            },


            {
                "code":"PERSONNEL_UNIT",
                "name":"واحد کارگزینی",
                "parent":"ADMIN_DEPARTMENT"
            },

            {
                "code":"TRAINING_WELFARE_UNIT",
                "name":"واحد آموزش و رفاه",
                "parent":"ADMIN_DEPARTMENT"
            },


            {
                "code":"ACCOUNTING_UNIT",
                "name":"واحد حسابداری",
                "parent":"FINANCE_DEPARTMENT"
            },

            {
                "code":"BUDGET_UNIT",
                "name":"واحد بودجه",
                "parent":"FINANCE_DEPARTMENT"
            },


            {
                "code":"SYSTEM_SUPPORT_UNIT",
                "name":"واحد پشتیبانی سامانه‌ها",
                "parent":"IT_DEPARTMENT"
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

                unit = OrganizationUnit(
                    code=item["code"],
                    name=item["name"],
                    unit_type="UNIT",
                    parent_id=parents[item["parent"]].id
                )

                db.add(unit)


        db.commit()

        print("Organization level 4 seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()

