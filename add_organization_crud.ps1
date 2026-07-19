Write-Host "=== ADD ORGANIZATION CRUD ==="

$base = "app\api\routes"

Write-Host "Creating organization CRUD route..."

@'
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.db.models.user import User
from app.db.models.organization import OrganizationUnit

router = APIRouter(
    prefix="/organization",
    tags=["organization-crud"]
)


@router.post("/")
def create_unit(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    unit = OrganizationUnit(
        name=data["name"],
        code=data.get("code"),
        parent_id=data.get("parent_id")
    )

    db.add(unit)
    db.commit()
    db.refresh(unit)

    return unit


@router.put("/{unit_id}")
def update_unit(
    unit_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    unit = db.query(OrganizationUnit).filter(
        OrganizationUnit.id == unit_id
    ).first()

    if not unit:
        raise HTTPException(404, "Unit not found")

    for key,value in data.items():
        if hasattr(unit,key):
            setattr(unit,key,value)

    db.commit()
    db.refresh(unit)

    return unit


@router.delete("/{unit_id}")
def delete_unit(
    unit_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):

    unit=db.query(OrganizationUnit).filter(
        OrganizationUnit.id==unit_id
    ).first()

    if not unit:
        raise HTTPException(404,"Unit not found")

    db.delete(unit)
    db.commit()

    return {
        "message":"deleted",
        "id":unit_id
    }
'@ | Set-Content "$base\organization_crud.py" -Encoding UTF8


Write-Host "Registering router..."

@'
from app.api.routes.organization_crud import router as organization_crud_router
'@ | Add-Content "app\main.py"


(Get-Content "app\main.py") `
-replace 'app.include_router\(\s*organization_router\s*\)',
'app.include_router(organization_router)`napp.include_router(organization_crud_router)' |
Set-Content "app\main.py"


Write-Host "DONE"