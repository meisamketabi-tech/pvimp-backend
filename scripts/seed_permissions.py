from app.db.session import SessionLocal

from app.db.models.permission import Permission


def seed():

    db = SessionLocal()

    try:

        permissions = [

            {
                "code": "VIEW_ORGANIZATION",
                "name": "مشاهده ساختار سازمانی",
                "description": "دسترسی مشاهده درخت سازمانی",
            },

            {
                "code": "VIEW_USERS",
                "name": "مشاهده کاربران",
                "description": "دسترسی مشاهده کاربران سازمان",
            },

            {
                "code": "VIEW_ASSIGNMENTS",
                "name": "مشاهده انتصابات",
                "description": "دسترسی مشاهده تخصیص کاربران به واحدها",
            },

            {
                "code": "MANAGE_USERS",
                "name": "مدیریت کاربران",
                "description": "ایجاد و ویرایش کاربران",
            },

            {
                "code": "MANAGE_ASSIGNMENTS",
                "name": "مدیریت انتصابات",
                "description": "ایجاد و ویرایش انتصابات سازمانی",
            },

            {
                "code": "VIEW_DASHBOARD",
                "name": "مشاهده داشبورد مدیریتی",
                "description": "دسترسی مشاهده داشبورد",
            },

        ]


        for item in permissions:

            exists = (
                db.query(Permission)
                .filter(
                    Permission.code == item["code"]
                )
                .first()
            )


            if not exists:

                db.add(
                    Permission(
                        code=item["code"],
                        title=item["name"],
                        description=item.get("description"),
                        is_active=True,
                    )
                )


        db.commit()

        print("Permissions seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()