from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models.user import User
from app.services.gis_disease_control_dashboard_service import GISDiseaseControlDashboardService


router = APIRouter(
    prefix="/gis/disease-control-dashboard",
    tags=["GIS Disease Control Dashboard"],
)


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
    # Authentication is enforced here. Scope enforcement can be tightened as
    # province/county organization assignments are populated; the response
    # already carries an explicit scope object for the frontend.
    return GISDiseaseControlDashboardService.dashboard(
        db=db,
        province_code=province_code,
        county_code=county_code,
        start_date=start_date,
        end_date=end_date,
        disease=disease,
        animal_type=animal_type,
    )
