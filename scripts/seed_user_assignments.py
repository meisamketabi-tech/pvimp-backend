from datetime import datetime

from app.db.session import SessionLocal

from app.db.models.user import User
from app.db.models.organization import OrganizationUnit
from app.db.models.role import Role
from app.db.models.assignment import UserAssignment


def seed():

    db = SessionLocal()

    try:

        assignments = [

            {
                "username": "general_director",
                "full_name": "مدیرکل دامپزشکی استان زنجان",
                "unit_code": "ZANJAN_VETERINARY_GENERAL_DIRECTORATE",
                "role_name": "مدیرکل دامپزشکی استان",
            },

            {
                "username": "health_deputy",
                "full_name": "معاون سلامت",
                "unit_code": "HEALTH_DEPUTY",
                "role_name": "معاون سلامت",
            },

            {
                "username": "public_health_head",
                "full_name": "رئیس اداره نظارت بر بهداشت عمومی و مواد غذایی",
                "unit_code": "PUBLIC_HEALTH_DEPARTMENT",
                "role_name": "رئیس اداره",
            },

        ]


        for item in assignments:


            user = (
                db.query(User)
                .filter(
                    User.username == item["username"]
                )
                .first()
            )


            if not user:

                user = User(
                    username=item["username"],
                    full_name=item["full_name"],
                    password_hash="TEMP_HASH",
                    is_active=True,
                )

                db.add(user)
                db.flush()



            unit = (
                db.query(OrganizationUnit)
                .filter(
                    OrganizationUnit.code == item["unit_code"]
                )
                .first()
            )


            role = (
                db.query(Role)
                .filter(
                    Role.name == item["role_name"]
                )
                .first()
            )


            if not unit or not role:
                continue



            exists = (
                db.query(UserAssignment)
                .filter(
                    UserAssignment.user_id == user.id,
                    UserAssignment.organization_unit_id == unit.id,
                    UserAssignment.role_id == role.id,
                )
                .first()
            )


            if not exists:

                db.add(
                    UserAssignment(
                        user_id=user.id,
                        organization_unit_id=unit.id,
                        role_id=role.id,
                        is_primary=True,
                        is_active=True,
                        start_date=datetime.utcnow(),
                    )
                )


        db.commit()

        print("User assignments seeded")


    finally:

        db.close()


if __name__ == "__main__":
    seed()