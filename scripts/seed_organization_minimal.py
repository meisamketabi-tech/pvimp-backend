from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit
from app.db.models.organization_level import OrganizationLevel
from app.db.models.organization_unit_type import OrganizationUnitType


def seed():

    db = SessionLocal()

    try:

        # levels
        general_level = (
            db.query(OrganizationLevel)
            .filter(
                OrganizationLevel.name == "اداره کل"
            )
            .first()
        )

        deputy_level = (
            db.query(OrganizationLevel)
            .filter(
                OrganizationLevel.name == "معاونت"
            )
            .first()
        )

        department_level = (
            db.query(OrganizationLevel)
            .filter(
                OrganizationLevel.name == "اداره"
            )
            .first()
        )


        # types
        office_type = (
            db.query(OrganizationUnitType)
            .first()
        )


        if not office_type:
            print("Organization type not found")
            return



        # اداره کل

        general = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.code ==
                "ZANJAN_VETERINARY_GENERAL_DIRECTORATE"
            )
            .first()
        )


        if not general:

            general = OrganizationUnit(
                name="اداره کل دامپزشکی استان زنجان",
                code="ZANJAN_VETERINARY_GENERAL_DIRECTORATE",
                unit_type="GENERAL_DIRECTORATE",
                type_id=office_type.id,
                level_id=general_level.id if general_level else None,
                is_active=True,
            )

            db.add(general)
            db.flush()



        # معاونت سلامت

        health = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.code=="HEALTH_DEPUTY"
            )
            .first()
        )


        if not health:

            health = OrganizationUnit(
                name="معاونت سلامت",
                code="HEALTH_DEPUTY",
                unit_type="DEPUTY",
                type_id=office_type.id,
                level_id=deputy_level.id if deputy_level else None,
                parent_id=general.id,
                is_active=True,
            )

            db.add(health)
            db.flush()



        # اداره بهداشت عمومی

        public_health = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.code=="PUBLIC_HEALTH_DEPARTMENT"
            )
            .first()
        )


        if not public_health:

            public_health = OrganizationUnit(
                name=
                "اداره نظارت بر بهداشت عمومی و مواد غذایی",
                code="PUBLIC_HEALTH_DEPARTMENT",
                unit_type="DEPARTMENT",
                type_id=office_type.id,
                level_id=
                department_level.id if department_level else None,
                parent_id=health.id,
                is_active=True,
            )

            db.add(public_health)


        db.commit()

        print("Organization units seeded")


    finally:
        db.close()



if __name__ == "__main__":
    seed()