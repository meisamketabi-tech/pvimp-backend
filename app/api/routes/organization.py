from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.organization_service import build_tree

from app.schemas.organization_tree import OrganizationTreeNode


router = APIRouter(
    prefix="/organization",
    tags=["Organization"],
)



@router.get(
    "/tree",
    response_model=list[OrganizationTreeNode],
)
def organization_tree(
    db: Session = Depends(get_db),
):

    return build_tree(db)
