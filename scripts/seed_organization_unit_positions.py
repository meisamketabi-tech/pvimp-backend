from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit
from app.db.models.organization_position import OrganizationPosition
from app.db.models.organization_unit_position import OrganizationUnitPosition


def add_position(db, unit_code, position_code):

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
        return


    exists = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.organization_unit_id == unit.id,
            OrganizationUnitPosition.organization_position_id == position.id
        )
        .first()
    )


    if not exists:

        db.add(
            OrganizationUnitPosition(
                organization_unit_id=unit.id,
                organization_position_id=position.id,
                is_active=True
            )
        )



def seed():

    db = SessionLocal()

    try:

        mappings = [

            ("GENERAL_DIRECTORATE","GENERAL_DIRECTOR"),

            ("HEALTH_DEPUTY","HEALTH_DEPUTY_MANAGER"),

            ("RESOURCE_DEPUTY","DEVELOPMENT_DEPUTY_MANAGER"),

            ("ANIMAL_HEALTH_DEPARTMENT","OFFICE_HEAD"),

            ("POULTRY_DEPARTMENT","OFFICE_HEAD"),

            ("PUBLIC_HEALTH_DEPARTMENT","OFFICE_HEAD"),

            ("DIAGNOSIS_DEPARTMENT","OFFICE_HEAD"),

            ("SUPPORT_DEPARTMENT","OFFICE_HEAD"),

            ("FINANCE_DEPARTMENT","OFFICE_HEAD"),

            ("IT_DEPARTMENT","OFFICE_HEAD"),

        ]


        for unit_code, position_code in mappings:

            add_position(
                db,
                unit_code,
                position_code
            )


        counties = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.unit_type=="COUNTY_OFFICE"
            )
            .all()
        )


        county_position = (
            db.query(OrganizationPosition)
            .filter(
                OrganizationPosition.code=="COUNTY_VETERINARY_HEAD"
            )
            .first()
        )


        if county_position:

            for county in counties:

                exists = (
                    db.query(OrganizationUnitPosition)
                    .filter(
                        OrganizationUnitPosition.organization_unit_id==county.id,
                        OrganizationUnitPosition.organization_position_id==county_position.id
                    )
                    .first()
                )


                if not exists:

                    db.add(
                        OrganizationUnitPosition(
                            organization_unit_id=county.id,
                            organization_position_id=county_position.id,
                            is_active=True
                        )
                    )


        db.commit()

        print("Organization unit positions seeded")


    finally:

        db.close()



if __name__=="__main__":
    seed()