from fastapi import APIRouter

# Core endpoints
from app.api.v1.endpoints import (
    assignment,
    geography,
    health,
    inspection,
    inspection_assignment,
    inspection_attachment,
    inspection_approval,
    inspection_comment,
    inspection_decision,
    inspection_followup,
    inspection_history,
    inspection_lab_result,
    inspection_notification,
    inspection_report,
    inspection_review,
    inspection_sample,
    inspection_schedule,
    inspection_template,
    inspection_violation,
    organization_geography,
    users,
)

# GIS endpoints
from app.api.v1.endpoints.gis import (
    gis_base,
    epidemiology_units,
    import_files,
    disease_report,
    vaccine_disposal,
    vaccine_inventory,
    vaccination_performance,
    vaccine_distribution,
    disease_occurrence,
    send_sample_detail,
    enable_care,
    slaughter_disposal,
    laboratory_result,
    spraying,
    vaccination_kpi,
    vaccination_overview,
)

# Authentication
from app.api.v1.auth.router import (
    router as auth_router,
)

# Organization
from app.api.v1.organization_tree import (
    router as organization_tree_router,
)

from app.api.v1.organization_positions import (
    router as organization_positions_router,
)

from app.api.v1.organization_users import (
    router as organization_users_router,
)

from app.api.v1.organization_responsibility import (
    router as organization_responsibility_router,
)

from app.api.v1.organization_dashboard import (
    router as organization_dashboard_router,
)

from app.api.v1.organization_unit_detail import (
    router as organization_unit_detail_router,
)

# Supervision
from app.api.v1 import supervision

api_router = APIRouter()

ROUTERS = [
    # Health
    health.router,
    # Inspection
    inspection.router,
    inspection_assignment.router,
    inspection_attachment.router,
    inspection_approval.router,
    inspection_comment.router,
    inspection_decision.router,
    inspection_followup.router,
    inspection_history.router,
    inspection_lab_result.router,
    inspection_notification.router,
    inspection_report.router,
    inspection_review.router,
    inspection_sample.router,
    inspection_schedule.router,
    inspection_template.router,
    inspection_violation.router,
    # GIS
    geography.router,
    organization_geography.router,
    vaccination_overview.router,
    vaccination_kpi.router,
    epidemiology_units.router,
    import_files.router,
    disease_report.router,
    vaccine_disposal.router,
    vaccine_inventory.router,
    vaccination_performance.router,
    vaccine_distribution.router,
    disease_occurrence.router,
    laboratory_result.router,
    send_sample_detail.router,
    enable_care.router,
    slaughter_disposal.router,
    spraying.router,
    # Organization
    organization_positions_router,
    organization_users_router,
    organization_responsibility_router,
    organization_tree_router,
    organization_dashboard_router,
    organization_unit_detail_router,
    # Assignment
    assignment.router,
    # Authentication
    auth_router,
    # Supervision
    supervision.router,
]

for router in ROUTERS:
    api_router.include_router(router)

# GIS base routes
api_router.include_router(gis_base.router)
