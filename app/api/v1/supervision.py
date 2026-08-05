from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.db.models.inspection import Inspection
from app.db.models.organization import OrganizationUnit
from app.db.models.user import User
from app.db.models.inspection import InspectionItemResult

router = APIRouter(prefix="/supervision", tags=["Supervision"])


@router.get("/inspections")
def get_supervision_dashboard(db: Session = Depends(get_db)):

    try:

        inspections = db.query(Inspection).order_by(Inspection.created_at.desc()).all()

    except Exception as e:
        raise

    result = []

    for item in inspections:

        unit_name = "-"
        unit = None

        if item.organization_unit_id:

            unit = (
                db.query(OrganizationUnit)
                .filter(OrganizationUnit.id == item.organization_unit_id)
                .first()
            )

            if unit:
                unit_name = unit.name

        inspector_name = "-"

        if item.inspector_id:

            user = db.query(User).filter(User.id == item.inspector_id).first()

            if user:
                inspector_name = user.full_name or user.username

        result.append(
            {
                "inspectionId": item.id,
                "inspectionNumber": item.inspection_number,
                "inspectionDate": item.inspection_date,
                "unitName": unit_name,
                "unitType": unit.unit_type if unit else "-",
                "inspectorName": inspector_name,
                "inspectionStatus": (
                    item.status.value if hasattr(item.status, "value") else item.status
                ),
                "nonComplianceCount": (
                    db.query(InspectionItemResult)
                    .filter(
                        InspectionItemResult.inspection_id == item.id,
                        InspectionItemResult.is_compliant == False,
                    )
                    .count()
                ),
                "judicialReferral": any(
                    getattr(v, "action_type", None) == "judicial"
                    for v in getattr(item, "violations", [])
                ),
                "sampling": bool(getattr(item, "samples", [])),
            }
        )

    return result
