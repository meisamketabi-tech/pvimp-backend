from app.db.session import SessionLocal

from app.db.models.role import Role
from app.db.models.permission import Permission
from app.db.models.role_permission import RolePermission


def seed():

    db = SessionLocal()

    try:

        mappings = [

            {
                "role": "مدیرکل دامپزشکی استان",
                "permissions": [
                    "VIEW_ORGANIZATION",
                    "VIEW_USERS",
                    "VIEW_ASSIGNMENTS",
                    "MANAGE_USERS",
                    "MANAGE_ASSIGNMENTS",
                    "VIEW_DASHBOARD",
                ],
            },

        ]


        for item in mappings:

            role = (
                db.query(Role)
                .filter(
                    Role.name == item["role"]
                )
                .first()
            )


            if not role:
                continue


            for permission_code in item["permissions"]:

                permission = (
                    db.query(Permission)
                    .filter(
                        Permission.code == permission_code
                    )
                    .first()
                )


                if not permission:
                    continue


                exists = (
                    db.query(RolePermission)
                    .filter(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == permission.id,
                    )
                    .first()
                )


                if not exists:

                    db.add(
                        RolePermission(
                            role_id=role.id,
                            permission_id=permission.id,
                            is_active=True,
                        )
                    )


        db.commit()

        print("Role permissions seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()