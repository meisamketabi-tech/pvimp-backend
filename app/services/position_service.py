
from sqlalchemy.orm import Session

from app.db.models.organization_position import OrganizationPosition
from app.db.models.organization_unit_position import OrganizationUnitPosition


class PositionService:

    def list_positions(self, db: Session):
        return (
            db.query(OrganizationPosition)
            .order_by(OrganizationPosition.id.asc())
            .all()
        )


    def create_position(self, db: Session, title: str, code: str):
        obj = OrganizationPosition(
            title=title,
            code=code,
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj


    def assign_position(
        self,
        db: Session,
        organization_unit_id: int,
        position_id: int,
    ):

        obj = OrganizationUnitPosition(
            organization_unit_id=organization_unit_id,
            organization_position_id=position_id,
            is_active=True,
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj


    def list_unit_positions(
        self,
        db: Session,
        organization_unit_id: int,
    ):

        return (
            db.query(OrganizationUnitPosition)
            .filter(
                OrganizationUnitPosition.organization_unit_id == organization_unit_id,
                OrganizationUnitPosition.is_active == True,
            )
            .all()
        )
