from app.db.session import SessionLocal

from app.db.models.organization_position import OrganizationPosition


def seed():

    db = SessionLocal()

    try:

        positions = [

            {
                "code": "GENERAL_DIRECTOR",
                "title": "مدیرکل دامپزشکی استان",
                "level_order": 1,
                "is_managerial": True,
            },

            {
                "code": "HEALTH_DEPUTY_MANAGER",
                "title": "معاون سلامت",
                "level_order": 2,
                "is_managerial": True,
            },

            {
                "code": "DEVELOPMENT_DEPUTY_MANAGER",
                "title": "معاون توسعه مدیریت و منابع",
                "level_order": 2,
                "is_managerial": True,
            },

            {
                "code": "OFFICE_HEAD",
                "title": "رئیس اداره",
                "level_order": 3,
                "is_managerial": True,
            },

            {
                "code": "COUNTY_VETERINARY_HEAD",
                "title": "رئیس اداره دامپزشکی شهرستان",
                "level_order": 3,
                "is_managerial": True,
            },

            {
                "code": "GROUP_HEAD",
                "title": "رئیس گروه",
                "level_order": 4,
                "is_managerial": True,
            },

            {
                "code": "RESPONSIBLE_EXPERT",
                "title": "کارشناس مسئول",
                "level_order": 5,
                "is_managerial": False,
            },

            {
                "code": "VETERINARIAN_EXPERT",
                "title": "کارشناس دامپزشکی",
                "level_order": 6,
                "is_managerial": False,
            },

            {
                "code": "INSPECTOR",
                "title": "بازرس بهداشتی",
                "level_order": 7,
                "is_managerial": False,
            },

            {
                "code": "ADMIN_EXPERT",
                "title": "کارشناس اداری",
                "level_order": 8,
                "is_managerial": False,
            },

        ]


        for item in positions:

            exists = (
                db.query(OrganizationPosition)
                .filter(
                    OrganizationPosition.code == item["code"]
                )
                .first()
            )


            if not exists:

                position = OrganizationPosition(
                    code=item["code"],
                    title=item["title"],
                    level_order=item["level_order"],
                    is_managerial=item["is_managerial"],
                    is_active=True,
                )

                db.add(position)


        db.commit()

        print("Organization positions seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()

