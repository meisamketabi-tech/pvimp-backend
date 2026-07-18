from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.models.org import County, Province, VeterinaryUnit
from app.db.models.user import Role, User, UserRole
from app.db.session import SessionLocal


def get_or_create_role(db: Session, name: str, description: str | None = None) -> Role:
    obj = db.query(Role).filter(Role.name == name).first()
    if obj:
        if description is not None and obj.description != description:
            obj.description = description
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj

    obj = Role(name=name, description=description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def assign_role(
    db: Session,
    user: User,
    role: Role,
    veterinary_unit_id: int | None = None,
) -> UserRole:
    obj = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user.id,
            UserRole.role_id == role.id,
            UserRole.veterinary_unit_id == veterinary_unit_id,
        )
        .first()
    )
    if obj:
        return obj

    obj = UserRole(
        user_id=user.id,
        role_id=role.id,
        veterinary_unit_id=veterinary_unit_id,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def seed(db: Session) -> None:
    province = db.query(Province).filter(Province.code == "ZNJ").first()
    if not province:
        province = Province(
            name="Zanjan",
            code="ZNJ",
            is_active=True,
        )
        db.add(province)
        db.commit()
        db.refresh(province)

    county = db.query(County).filter(County.code == "ZNJ-01").first()
    if not county:
        county = County(
            name="Zanjan County",
            code="ZNJ-01",
            province_id=province.id,
            is_active=True,
        )
        db.add(county)
        db.commit()
        db.refresh(county)

    unit = db.query(VeterinaryUnit).filter(VeterinaryUnit.code == "VU-ZNJ-01").first()
    if not unit:
        unit = VeterinaryUnit(
            name="Zanjan Veterinary Unit",
            code="VU-ZNJ-01",
            unit_type="PROVINCIAL",
            county_id=county.id,
            is_active=True,
        )
        db.add(unit)
        db.commit()
        db.refresh(unit)

    province_admin_role = get_or_create_role(db, "PROVINCE_ADMIN", "Province administrator")
    unit_manager_role = get_or_create_role(db, "UNIT_MANAGER", "Veterinary unit manager")
    viewer_role = get_or_create_role(db, "VIEWER", "Read-only access")

    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            full_name="System Admin",
            email="admin@example.com",
            mobile=None,
            is_active=True,
            password_hash=get_password_hash("Admin@12345"),
            default_veterinary_unit_id=unit.id,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

    assign_role(db, admin_user, province_admin_role, veterinary_unit_id=unit.id)
    assign_role(db, admin_user, unit_manager_role, veterinary_unit_id=unit.id)
    assign_role(db, admin_user, viewer_role, veterinary_unit_id=unit.id)


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
        print("Seed completed successfully.")
        db.commit()
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()
