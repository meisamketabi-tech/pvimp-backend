from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit
from app.db.models.organization_position import OrganizationPosition
from app.db.models.organization_unit_position import OrganizationUnitPosition


def seed():

    db = SessionLocal()

    try:

        mappings = [

            (
                "ZANJAN_VETERINARY_GENERAL_DIRECTORATE",
                "GENERAL_DIRECTOR"
            ),

            (
                "HEALTH_DEPUTY",
                "HEALTH_DEPUTY_MANAGER"
            ),

            (
                "DEVELOPMENT_DEPUTY",
                "DEVELOPMENT_DEPUTY_MANAGER"
            ),

            (
                "ANIMAL_HEALTH_DEPARTMENT",
                "OFFICE_HEAD"
            ),

            (
                "POULTRY_HEALTH_DEPARTMENT",
                "OFFICE_HEAD"
            ),

            (
                "PUBLIC_HEALTH_DEPARTMENT",
                "OFFICE_HEAD"
            ),

            (
                "QUARANTINE_DEPARTMENT",
                "OFFICE_HEAD"
            ),

            (
                "ADMIN_DEPARTMENT",
                "OFFICE_HEAD"
            ),

            (
                "FINANCE_DEPARTMENT",
                "OFFICE_HEAD"
            ),

            (
                "IT_DEPARTMENT",
                "OFFICE_HEAD"
            ),

        ]


        for unit_code, position_code in mappings:

            unit = (
                db.query(OrganizationUnit)
                .filter(
                    OrganizationUnit.code == unit_code
                )
                .first()
            )


            position = (
                db.query(OrganizationPosition)
                .filter(
                    OrganizationPosition.code == position_code
                )
                .first()
            )


            if not unit or not position:
                continue


            exists = (
                db.query(OrganizationUnitPosition)
                .filter(
                    OrganizationUnitPosition.organization_unit_id == unit.id,
                    OrganizationUnitPosition.organization_position_id == position.id,
                )
                .first()
            )


            if not exists:

                db.add(
                    OrganizationUnitPosition(
                        organization_unit_id=unit.id,
                        organization_position_id=position.id,
                        is_active=True,
                    )
                )



        county_units = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.unit_type == "COUNTY_OFFICE"
            )
            .all()
        )


        county_position = (
            db.query(OrganizationPosition)
            .filter(
                OrganizationPosition.code == "COUNTY_VETERINARY_HEAD"
            )
            .first()
        )


        if county_position:

            for county in county_units:

                exists = (
                    db.query(OrganizationUnitPosition)
                    .filter(
                        OrganizationUnitPosition.organization_unit_id == county.id,
                        OrganizationUnitPosition.organization_position_id == county_position.id,
                    )
                    .first()
                )


                if not exists:

                    db.add(
                        OrganizationUnitPosition(
                            organization_unit_id=county.id,
                            organization_position_id=county_position.id,
                            is_active=True,
                        )
                    )


        db.commit()

        print("Organization unit positions seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()

