from fastapi import APIRouter

from app.db.session import SessionLocal
from app.db.models.organization_unit_position import OrganizationUnitPosition


router = APIRouter(
    prefix="/organization",
    tags=["Organization"]
)


@router.get("/{unit_id}/positions")
def get_unit_positions(unit_id: int):

    db = SessionLocal()

    try:

        items = (
            db.query(OrganizationUnitPosition)
            .filter(
                OrganizationUnitPosition.organization_unit_id == unit_id,
                OrganizationUnitPosition.is_active == True,
            )
            .all()
        )


        result = []


        for item in items:

            result.append(
                {
                    "id": item.id,
                    "position_id": item.organization_position.id,
                    "position_code": item.organization_position.code,
                    "position_title": item.organization_position.title,
                }
            )


        return result


    finally:

        db.close()

