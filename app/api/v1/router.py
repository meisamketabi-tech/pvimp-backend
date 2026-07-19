from app.api.v1.organization_unit_detail import router as organization_unit_detail_router
from fastapi import APIRouter
from app.api.v1.organization_dashboard import router as organization_dashboard_router
from app.api.v1.endpoints import users
from app.api.v1.endpoints import assignment

from app.api.v1.auth import router as auth_router

from app.api.v1.organization_tree import router as organization_tree_router

from app.api.v1.organization_positions import (
    router as organization_positions_router
)

from app.api.v1.organization_users import (
    router as organization_users_router
)

from app.api.v1.endpoints import (
    health,
    inspection,
    inspection_assignment,
    inspection_attachment,
    inspection_approval,
    inspection_report,
    inspection_violation,
    inspection_followup,
    inspection_history,
    inspection_comment,
    inspection_sample,
    inspection_lab_result,
    inspection_schedule,
    inspection_template,
    inspection_decision,
    inspection_review,
    inspection_notification,
)


api_router = APIRouter()


api_router.include_router(
    health.router
)

api_router.include_router(
    inspection.router
)

api_router.include_router(
    inspection_assignment.router
)

api_router.include_router(
    inspection_attachment.router
)

api_router.include_router(
    inspection_approval.router
)

api_router.include_router(
    inspection_report.router
)

api_router.include_router(
    inspection_violation.router
)

api_router.include_router(
    inspection_followup.router
)

api_router.include_router(
    inspection_history.router
)

api_router.include_router(
    inspection_comment.router
)

api_router.include_router(
    inspection_sample.router
)

api_router.include_router(
    inspection_lab_result.router
)

api_router.include_router(
    inspection_schedule.router
)

api_router.include_router(
    inspection_template.router
)

api_router.include_router(
    inspection_decision.router
)

api_router.include_router(
    inspection_review.router
)

api_router.include_router(
    inspection_notification.router
)


api_router.include_router(
    organization_positions_router
)

api_router.include_router(
    organization_users_router
)


api_router.include_router(
    organization_tree_router
)


api_router.include_router(
    assignment.router
)


api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)


api_router.include_router(
    auth_router.router
)


api_router.include_router(
    organization_dashboard_router
)


api_router.include_router(
    organization_unit_detail_router
)