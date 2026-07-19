from app.db.session import SessionLocal
from app.db.models.role import Role


def seed():

    db = SessionLocal()

    roles = [
        {
            "name": "مدیرکل دامپزشکی استان",
            "description": "مدیر ارشد اداره کل",
        },
        {
            "name": "معاون سلامت",
            "description": "مدیریت معاونت سلامت",
        },
        {
            "name": "رئیس اداره",
            "description": "رئیس اداره تخصصی",
        },
    ]


    try:

        for item in roles:

            exists = (
                db.query(Role)
                .filter(
                    Role.name == item["name"]
                )
                .first()
            )

            if not exists:

                db.add(
                    Role(**item)
                )


        db.commit()

        print("Roles seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()