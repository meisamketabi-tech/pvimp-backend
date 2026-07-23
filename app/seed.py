from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.db.models.user import User


def seed(db: Session):

    user = db.query(User).filter(
        User.username == "admin"
    ).first()

    if user:
        user.password_hash = get_password_hash("Admin@12345")
        user.is_active = True
        db.commit()
        print("Admin password reset completed")
        return

    user = User(
        username="admin",
        full_name="System Admin",
        email="admin@example.com",
        mobile=None,
        is_active=True,
        password_hash=get_password_hash("Admin@12345"),
    )

    db.add(user)
    db.commit()

    print("Admin user created")


if __name__ == "__main__":

    db = SessionLocal()

    try:
        seed(db)

    finally:
        db.close()
