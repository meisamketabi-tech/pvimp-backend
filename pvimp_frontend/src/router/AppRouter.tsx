import React, { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import AuthGuard from "../components/auth/AuthGuard";

const LoginV2 = lazy(() => import("../pages/LoginV2"));
const Dashboard = lazy(() => import("../pages/Dashboard"));
const HealthDeputyDashboard = lazy(() => import("../pages/HealthDeputyDashboard"));
const DiseaseControlExpertDashboard = lazy(() => import("../pages/DiseaseControlExpertDashboard"));
const QuarantineExpertDashboard = lazy(() => import("../pages/QuarantineExpertDashboard"));
const PoultryExpertDashboard = lazy(() => import("../pages/PoultryExpertDashboard"));
const DiagnosisExpertDashboard = lazy(() => import("../pages/DiagnosisExpertDashboard"));
const LabExpertDashboard = lazy(() => import("../pages/LabExpertDashboard"));
const GISDashboard = lazy(() => import("../pages/GISDashboard"));
const GISDepartmentList = lazy(() => import("../pages/GISDepartmentList"));
const GISDepartmentDetail = lazy(() => import("../pages/GISDepartmentDetail"));
const GISDepartmentUpload = lazy(() => import("../pages/GISDepartmentUpload"));
const GISCountyDashboard = lazy(() => import("../pages/GISCountyDashboard"));
const VaccinationKpiDrilldown = lazy(() => import("../pages/VaccinationKpiDrilldown"));
const VaccinationVaccineReport = lazy(() => import("../pages/VaccinationVaccineReport"));
const KPIAnalysis = lazy(() => import("../pages/KPIAnalysis"));
const KpiDetail = lazy(() => import("../pages/KpiDetail"));
const GISCountyDetailDashboard = lazy(() => import("../pages/GISCountyDetailDashboard"));
const CountyDashboard = lazy(() => import("../pages/CountyDashboard"));
const SupervisionDashboard = lazy(() => import("../pages/SupervisionDashboard"));
const SupervisionInspectionCreate = lazy(() => import("../pages/SupervisionInspectionCreate"));
const SupervisionInspectionList = lazy(() => import("../pages/SupervisionInspectionList"));
const SupervisionReports = lazy(() => import("../pages/SupervisionReports"));
const SupervisionGISDashboard = lazy(() => import("../pages/SupervisionGISDashboard"));
const SupervisionViolations = lazy(() => import("../pages/SupervisionViolations"));
const SupervisionSamples = lazy(() => import("../pages/SupervisionSamples"));
const SupervisionLegal = lazy(() => import("../pages/SupervisionLegal"));
const SupervisionSettings = lazy(() => import("../pages/SupervisionSettings"));
const SupervisionStatistics = lazy(() => import("../pages/SupervisionStatistics"));
const SupervisionNationalDashboard = lazy(() => import("../pages/SupervisionNationalDashboard"));
const SupervisionExecutiveReports = lazy(() => import("../pages/SupervisionExecutiveReports"));
const SupervisionOrganizationChart = lazy(() => import("../pages/SupervisionOrganizationChart"));
const SupervisionProvinceView = lazy(() => import("../pages/SupervisionProvinceView"));
const SupervisionCountyView = lazy(() => import("../pages/SupervisionCountyView"));
const SupervisionMasterReports = lazy(() => import("../pages/SupervisionMasterReports"));
const SupervisionPortal = lazy(() => import("../pages/SupervisionPortal"));
const SupervisionTrendAnalysis = lazy(() => import("../pages/SupervisionTrendAnalysis"));
const SupervisionNationalKPIs = lazy(() => import("../pages/SupervisionNationalKPIs"));
const SupervisionAnalyticsCenter = lazy(() => import("../pages/SupervisionAnalyticsCenter"));
const SupervisionControlRoom = lazy(() => import("../pages/SupervisionControlRoom"));
const SupervisionAIAnalysis = lazy(() => import("../pages/SupervisionAIAnalysis"));
const SupervisionRiskDashboard = lazy(() => import("../pages/SupervisionRiskDashboard"));
const SupervisionOperationalDashboard = lazy(() => import("../pages/SupervisionOperationalDashboard"));
const SupervisionForm = lazy(() => import("../pages/SupervisionForm"));
const SupervisionGISImport = lazy(() => import("../pages/SupervisionGISImport"));
const ResponsibleHealthDashboard = lazy(() => import("../pages/ResponsibleHealthDashboard"));

function RouteFallback() {
  return (
    <div style={{ minHeight: "40vh", display: "grid", placeItems: "center" }} dir="rtl">
      در حال بارگذاری صفحه...
    </div>
  );
}

export default function AppRouter() {
  return (
    <Suspense fallback={<RouteFallback />}>
      <Routes>
        <Route path="/login" element={<LoginV2 />} />
        <Route element={<AuthGuard />}>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="health-deputy" element={<HealthDeputyDashboard />} />
            <Route path="disease-control" element={<DiseaseControlExpertDashboard />} />
            <Route path="quarantine" element={<QuarantineExpertDashboard />} />
            <Route path="poultry" element={<PoultryExpertDashboard />} />
            <Route path="diagnosis" element={<DiagnosisExpertDashboard />} />
            <Route path="laboratory" element={<LabExpertDashboard />} />
            <Route path="gis" element={<GISDashboard />} />
            <Route path="gis/departments" element={<GISDepartmentList />} />
            <Route path="gis/kpi/vaccination/drilldown/:view" element={<VaccinationKpiDrilldown />} />
            <Route path="gis/kpi/vaccination/drilldown/:view/:code" element={<VaccinationKpiDrilldown />} />
            <Route path="gis/kpi/vaccination/vaccine/:vaccineType" element={<VaccinationVaccineReport />} />
            <Route path="gis/kpi/vaccination/vaccines" element={<VaccinationVaccineReport />} />
            <Route path="gis/kpi/vaccination" element={<KPIAnalysis />} />
            <Route path="gis/kpi/vaccination/unit/:unitCode" element={<KpiDetail />} />
            <Route path="gis/department/:code" element={<GISDepartmentDetail />} />
            <Route path="gis/upload/:department" element={<GISDepartmentUpload />} />
            <Route path="supervision" element={<SupervisionDashboard />} />
            <Route path="supervision/create" element={<SupervisionInspectionCreate />} />
            <Route path="supervision/list" element={<SupervisionInspectionList />} />
            <Route path="supervision/reports" element={<SupervisionReports />} />
            <Route path="supervision/gis" element={<SupervisionGISDashboard />} />
            <Route path="supervision/violations" element={<SupervisionViolations />} />
            <Route path="supervision/samples" element={<SupervisionSamples />} />
            <Route path="supervision/legal" element={<SupervisionLegal />} />
            <Route path="supervision/settings" element={<SupervisionSettings />} />
            <Route path="supervision/statistics" element={<SupervisionStatistics />} />
            <Route path="supervision/national-dashboard" element={<SupervisionNationalDashboard />} />
            <Route path="supervision/executive-reports" element={<SupervisionExecutiveReports />} />
            <Route path="supervision/organization-chart" element={<SupervisionOrganizationChart />} />
            <Route path="supervision/forms" element={<SupervisionForm />} />
            <Route path="supervision/province-view" element={<SupervisionProvinceView />} />
            <Route path="supervision/county-view" element={<SupervisionCountyView />} />
            <Route path="supervision/master-reports" element={<SupervisionMasterReports />} />
            <Route path="supervision/portal" element={<SupervisionPortal />} />
            <Route path="supervision/trend-analysis" element={<SupervisionTrendAnalysis />} />
            <Route path="supervision/national-kpis" element={<SupervisionNationalKPIs />} />
            <Route path="supervision/analytics-center" element={<SupervisionAnalyticsCenter />} />
            <Route path="supervision/control-room" element={<SupervisionControlRoom />} />
            <Route path="supervision/ai-analysis" element={<SupervisionAIAnalysis />} />
            <Route path="supervision/risk-dashboard" element={<SupervisionRiskDashboard />} />
            <Route path="supervision/operational-dashboard" element={<SupervisionOperationalDashboard />} />
            <Route path="county/:id/gis-dashboard" element={<GISCountyDetailDashboard />} />
            <Route path="county/:id/gis-detail" element={<GISCountyDetailDashboard />} />
            <Route path="county/:id" element={<CountyDashboard />} />
            <Route path="county/:id/deputy" element={<CountyDashboard />} />
            <Route path="responsible-health" element={<ResponsibleHealthDashboard />} />
            <Route path="county/:id/expert/supervision/import" element={<SupervisionGISImport />} />
          </Route>
          <Route path="/gis-county-dashboard" element={<GISCountyDashboard />} />
        </Route>
      </Routes>
    </Suspense>
  );
}
