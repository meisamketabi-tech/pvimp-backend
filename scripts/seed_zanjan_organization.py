from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.db.models.organization import OrganizationUnit
from app.db.models.organization_unit_type import OrganizationUnitType
from app.db.models.organization_level import OrganizationLevel


def get_type(db, code):
    return (
        db.query(OrganizationUnitType)
        .filter(
            OrganizationUnitType.code == code
        )
        .first()
    )


def get_level(db, order):
    return (
        db.query(OrganizationLevel)
        .filter(
            OrganizationLevel.level_order == order
        )
        .first()
    )


def create_unit(
    db,
    name,
    code,
    type_code,
    level_order,
    parent=None,
):

    exists = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.code == code
        )
        .first()
    )

    if exists:
        return exists


    unit = OrganizationUnit(
        name=name,
        code=code,
        unit_type=type_code,
        type_id=get_type(db, type_code).id,
        level_id=get_level(db, level_order).id,
        parent_id=parent.id if parent else None,
    )

    db.add(unit)
    db.flush()

    return unit



def seed():

    db: Session = SessionLocal()

    try:

        general = create_unit(
            db,
            "اداره کل دامپزشکی استان زنجان",
            "ZANJAN_GENERAL_DIRECTORATE",
            "GENERAL_DIRECTORATE",
            1,
        )


        health = create_unit(
            db,
            "معاونت سلامت",
            "HEALTH_DEPUTY",
            "DEPUTY",
            2,
            general,
        )


        public_health = create_unit(
            db,
            "اداره نظارت بر بهداشت عمومی و مواد غذایی",
            "PUBLIC_HEALTH_DEPARTMENT",
            "DEPARTMENT",
            4,
            health,
        )


        quarantine = create_unit(
            db,
            "اداره قرنطینه و امنیت زیستی",
            "QUARANTINE_DEPARTMENT",
            "DEPARTMENT",
            4,
            health,
        )


        development = create_unit(
            db,
            "معاونت توسعه مدیریت و منابع",
            "DEVELOPMENT_DEPUTY",
            "DEPUTY",
            2,
            general,
        )


        db.commit()


    finally:
        db.close()



if __name__ == "__main__":
    seed()
