from datetime import datetime

from app.db.session import SessionLocal

from app.db.models.user import User
from app.db.models.organization import OrganizationUnit
from app.db.models.role import Role
from app.db.models.assignment import UserAssignment


def assign_admin():

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.username == "admin")
            .first()
        )

        if not user:
            print("Admin user not found")
            return


        unit = (
            db.query(OrganizationUnit)
            .filter(
                OrganizationUnit.code ==
                "ZANJAN_VETERINARY_GENERAL_DIRECTORATE"
            )
            .first()
        )


        role = (
            db.query(Role)
            .filter(
                Role.name ==
                "مدیرکل دامپزشکی استان"
            )
            .first()
        )


        if not unit:
            print("Organization unit not found")
            return


        if not role:
            print("Role not found")
            return


        exists = (
            db.query(UserAssignment)
            .filter(
                UserAssignment.user_id == user.id,
                UserAssignment.organization_unit_id == unit.id,
                UserAssignment.role_id == role.id,
                UserAssignment.is_active.is_(True),
            )
            .first()
        )


        if exists:
            print("Admin assignment already exists")
            return


        assignment = UserAssignment(
            user_id=user.id,
            organization_unit_id=unit.id,
            role_id=role.id,
            is_primary=True,
            is_active=True,
            start_date=datetime.utcnow(),
        )


        db.add(assignment)
        db.commit()

        print("Admin assignment created successfully")


    finally:
        db.close()


if __name__ == "__main__":
    assign_admin()