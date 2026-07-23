from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router

from app.api import (
    outbreaks,
    diseases,
    vaccines,
    farms,
    animals,
    veterinary_centers,
    quarantine,
    samples,
    backups,
    events,
    workflows,
    dashboards,
    sync,
    reports,
    complaints,
    profiles,
    assignments,
    planning,
    legal,
    violations,
    laboratory,
    locations,
    inventory,
    exports,
    permissions,
    templates,
    messages,
    files,
    config,
    workflow_designer,
    search,
    automation,
    backup,
    mobile,
    notifications,
    integrations,
    knowledge,
    complaint_workflow,
    analytics,
    work_orders,
    organization,
    system,
    calendar,
    kpi,
    documents,
    approvals,
    report_builder,
    checklists,
    units,
    inspections,
    licenses,
    lims,
    gis,
    tasks,
    alerts,
    inspection_forms,
    workflow_runtime,
    security,
    ai,
    integration,
    dashboard,
    capa,
    sampling,
    complaint,
    notification,
    audit,
    form_builder,
    responsible_health_unit,
    inspection_result,
    health_alert,
    violation_followup,
    inspection_schedule,
    audit_log,
    personnel,
    cold_chain,
    action_plan,
    inspection,
    export_report,
    reminder,
    score,
    training,
    risk,
    schedule,
    workflow,
    responsible_health,
    dynamic_forms,
    rules,
    inspection_plan,
    lab
)

from app.api.routes.organization import router as organization_router
from app.api.routes.organization_crud import router as organization_crud_router
from app.api.routes.position import router as position_router


app = FastAPI(
    title=settings.APP_NAME
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api/v1")

app.include_router(organization_router)
app.include_router(organization_crud_router)
app.include_router(position_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.APP_NAME} is running"
    }


routers = [
    responsible_health.router,
    audit.router,
    workflow.router,
    notification.router,
    schedule.router,
    risk.router,
    complaint.router,
    training.router,
    score.router,
    reminder.router,
    export_report.router,
    inspection.router,
    action_plan.router,
    sampling.router,
    cold_chain.router,
    personnel.router,
    audit_log.router,
    inspection_schedule.router,
    violation_followup.router,
    health_alert.router,
    inspection_result.router,
    responsible_health_unit.router,
    dynamic_forms.router,
    rules.router,
    form_builder.router,
    inspection_plan.router,
    capa.router,
    dashboard.router,
    reports.router,
    integration.router,
    ai.router,
    security.router,
    files.router,
    workflow_runtime.router,
    inspection_forms.router,
    alerts.router,
    tasks.router,
    messages.router,
    gis.router,
    lims.router,
    licenses.router,
    inspections.router,
    violations.router,
    units.router,
    checklists.router,
    report_builder.router,
    documents.router,
    approvals.router,
    kpi.router,
    calendar.router,
    system.router,
    organization.router,
    work_orders.router,
    analytics.router,
    complaint_workflow.router,
    knowledge.router,
    integrations.router,
    notifications.router,
    mobile.router,
    backup.router,
    automation.router,
    search.router,
    workflow_designer.router,
    config.router,
    templates.router,
    permissions.router,
    exports.router,
    inventory.router,
    locations.router,
    laboratory.router,
    legal.router,
    planning.router,
    assignments.router,
    profiles.router,
    complaints.router,
    sync.router,
    dashboards.router,
    workflows.router,
    events.router,
    backups.router,
    samples.router,
    lab.router,
    quarantine.router,
    veterinary_centers.router,
    animals.router,
    farms.router,
    vaccines.router,
    diseases.router,
    outbreaks.router,
]


for router in routers:
    app.include_router(router)