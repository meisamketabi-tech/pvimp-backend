from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_active_assignments, get_current_user, get_db
from app.db.models.gis_county import GISCounty
from app.db.models.gis_province import GISProvince
from app.db.models.user import User
from app.services.gis_disease_control_dashboard_service import GISDiseaseControlDashboardService

router = APIRouter(
    prefix="/gis/disease-control-dashboard",
    tags=["GIS Disease Control Dashboard"],
)

GLOBAL_ROLES = {"admin", "director_general", "health_deputy", "مدیرکل دامپزشکی استان", "معاون سلامت"}
PROVINCE_ROLES = {"disease_control_expert", "کارشناس مبارزه با بیماری‌های دامی", "اداره مبارزه با بیماری‌های دامی"}
COUNTY_ROLES = {"county_head", "رئیس اداره"}


def _role_names(assignments):
    return {a.role.name.strip().lower() for a in assignments if a.role and a.role.name}


def _scope_for_user(db: Session, user: User, province_code: str | None, county_code: str | None):
    assignments = get_active_assignments(db, user)
    roles = _role_names(assignments)

    if roles.intersection({x.lower() for x in GLOBAL_ROLES}):
        return province_code, county_code

    if roles.intersection({x.lower() for x in PROVINCE_ROLES}):
        province_ids = {a.organization_unit.province_id for a in assignments if a.organization_unit and a.organization_unit.province_id is not None}
        if not province_ids:
            raise HTTPException(403, "استان محل خدمت برای کاربر مشخص نشده است")
        provinces = db.query(GISProvince).filter(GISProvince.id.in_(province_ids)).all()
        allowed_codes = {p.province_code for p in provinces}
        if province_code and province_code not in allowed_codes:
            raise HTTPException(403, "دسترسی به این استان مجاز نیست")
        if county_code:
            county = db.query(GISCounty).filter(GISCounty.county_code == county_code).first()
            if not county or county.province_id not in province_ids:
                raise HTTPException(403, "دسترسی به این شهرستان مجاز نیست")
        return province_code or (next(iter(allowed_codes)) if len(allowed_codes) == 1 else None), county_code

    if roles.intersection({x.lower() for x in COUNTY_ROLES}):
        county_ids = {a.organization_unit.county_id for a in assignments if a.organization_unit and a.organization_unit.county_id is not None}
        if not county_ids:
            raise HTTPException(403, "شهرستان محل خدمت برای کاربر مشخص نشده است")
        counties = db.query(GISCounty).filter(GISCounty.id.in_(county_ids)).all()
        allowed_codes = {c.county_code for c in counties}
        if county_code and county_code not in allowed_codes:
            raise HTTPException(403, "دسترسی به این شهرستان مجاز نیست")
        return province_code, county_code or (next(iter(allowed_codes)) if len(allowed_codes) == 1 else None)

    raise HTTPException(403, "نقش کاربر برای مشاهده داشبورد مبارزه با بیماری‌های دامی مجاز نیست")


@router.get("/summary")
def get_dashboard_summary(
    province_code: str | None = Query(default=None),
    county_code: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    disease: str | None = Query(default=None),
    animal_type: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    province_code, county_code = _scope_for_user(db, current_user, province_code, county_code)
    return GISDiseaseControlDashboardService.dashboard(
        db=db,
        province_code=province_code,
        county_code=county_code,
        start_date=start_date,
        end_date=end_date,
        disease=disease,
        animal_type=animal_type,
    )
