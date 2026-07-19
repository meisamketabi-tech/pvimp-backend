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


        units = [

            {
                "code": "HEALTH_DEPUTY",
                "name": "معاونت سلامت",
                "unit_type": "DEPUTY",
            },

            {
                "code": "DEVELOPMENT_DEPUTY",
                "name": "معاونت توسعه مدیریت و منابع",
                "unit_type": "DEPUTY",
            },

            {
                "code": "MANAGEMENT_OFFICE",
                "name": "حوزه مدیریت",
                "unit_type": "UNIT",
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
                    unit_type=item["unit_type"],
                    parent_id=root.id,
                )

                db.add(unit)


        db.commit()

        print("Organization level 2 seeded")


    finally:
        db.close()


if __name__ == "__main__":
    seed()
