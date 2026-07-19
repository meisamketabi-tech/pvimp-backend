from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit


def seed():

    db = SessionLocal()

    try:

        county_units = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.unit_type == "COUNTY_OFFICE"
            )
            .all()
        )


        units = []

        for county in county_units:

            units.append(
                {
                    "code": f"{county.code}_INSPECTION",
                    "name": f"واحد نظارت و بازرسی {county.name.replace('اداره دامپزشکی شهرستان ','')}",
                    "parent_id": county.id,
                }
            )

            units.append(
                {
                    "code": f"{county.code}_EPIDEMIOLOGY",
                    "name": f"واحد بهداشت و بیماری‌ها {county.name.replace('اداره دامپزشکی شهرستان ','')}",
                    "parent_id": county.id,
                }
            )


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
                    parent_id=item["parent_id"],
                )

                db.add(unit)


        db.commit()

        print("County internal units seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()

