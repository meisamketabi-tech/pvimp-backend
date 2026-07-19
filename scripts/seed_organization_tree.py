from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit
from app.db.models.organization_unit_type import OrganizationUnitType
from app.db.models.organization_level import OrganizationLevel


def seed():

    db = SessionLocal()

    try:

        general_type = (
            db.query(OrganizationUnitType)
            .filter(
                OrganizationUnitType.code == "GENERAL_DIRECTORATE"
            )
            .first()
        )


        general_level = (
            db.query(OrganizationLevel)
            .filter(
                OrganizationLevel.code == "GENERAL_DIRECTORATE"
            )
            .first()
        )


        root_unit = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.code ==
                "ZANJAN_VETERINARY_GENERAL_DIRECTORATE"
            )
            .first()
        )


        if not root_unit:

            root_unit = OrganizationUnit(
                code="ZANJAN_VETERINARY_GENERAL_DIRECTORATE",
                name="اداره کل دامپزشکی استان زنجان",
                unit_type="GENERAL_DIRECTORATE",
                type_id=general_type.id,
                level_id=general_level.id,
                parent_id=None,
            )

            db.add(root_unit)

        else:

            root_unit.type_id = general_type.id
            root_unit.level_id = general_level.id


        db.commit()

        print("Organization root updated")


    finally:
        db.close()


if __name__ == "__main__":
    seed()
