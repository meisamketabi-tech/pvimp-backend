import React from "react";
import { Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import MainLayout from "../layouts/MainLayout";
import Dashboard from "../pages/Dashboard";
import AuthGuard from "../components/auth/AuthGuard";
import GISDashboard from "../pages/GISDashboard";
import GISDepartmentList from "../pages/GISDepartmentList";
import GISDepartmentDetail from "../pages/GISDepartmentDetail";
import GISDepartmentUpload from "../pages/GISDepartmentUpload";
import GISCountyDashboard from "../pages/GISCountyDashboard";
import VaccinationKpiDrilldown from "../pages/VaccinationKpiDrilldown";
import VaccinationVaccineReport from "../pages/VaccinationVaccineReport";
import GISCountyDetailDashboard from "../pages/GISCountyDetailDashboard";
import KPIAnalysis from "../pages/KPIAnalysis";
import KpiDetail from "../pages/KpiDetail";
import CountyDashboard from "../pages/CountyDashboard";
import SupervisionDashboard from "../pages/SupervisionDashboard";
import SupervisionInspectionCreate from "../pages/SupervisionInspectionCreate";
import SupervisionInspectionList from "../pages/SupervisionInspectionList";
import SupervisionReports from "../pages/SupervisionReports";
import SupervisionGISDashboard from "../pages/SupervisionGISDashboard";
import SupervisionViolations from "../pages/SupervisionViolations";
import SupervisionSamples from "../pages/SupervisionSamples";
import SupervisionLegal from "../pages/SupervisionLegal";
import SupervisionSettings from "../pages/SupervisionSettings";
import SupervisionStatistics from "../pages/SupervisionStatistics";
import SupervisionNationalDashboard from "../pages/SupervisionNationalDashboard";
import SupervisionExecutiveReports from "../pages/SupervisionExecutiveReports";
import SupervisionOrganizationChart from "../pages/SupervisionOrganizationChart";
import SupervisionProvinceView from "../pages/SupervisionProvinceView";
import SupervisionCountyView from "../pages/SupervisionCountyView";
import SupervisionMasterReports from "../pages/SupervisionMasterReports";
import SupervisionPortal from "../pages/SupervisionPortal";
import SupervisionTrendAnalysis from "../pages/SupervisionTrendAnalysis";
import SupervisionNationalKPIs from "../pages/SupervisionNationalKPIs";
import SupervisionAnalyticsCenter from "../pages/SupervisionAnalyticsCenter";
import SupervisionControlRoom from "../pages/SupervisionControlRoom";
import SupervisionAIAnalysis from "../pages/SupervisionAIAnalysis";
import SupervisionRiskDashboard from "../pages/SupervisionRiskDashboard";
import SupervisionOperationalDashboard from "../pages/SupervisionOperationalDashboard";
import DiseaseControlExpertDashboard from "../pages/DiseaseControlExpertDashboard";
import HealthDeputyDashboard from "../pages/HealthDeputyDashboard";
import QuarantineExpertDashboard from "../pages/QuarantineExpertDashboard";
import PoultryExpertDashboard from "../pages/PoultryExpertDashboard";
import DiagnosisExpertDashboard from "../pages/DiagnosisExpertDashboard";
import LabExpertDashboard from "../pages/LabExpertDashboard";
import SupervisionForm from "../pages/SupervisionForm";
import SupervisionGISImport from "../pages/SupervisionGISImport";
import ResponsibleHealthDashboard from "../pages/ResponsibleHealthDashboard";

export default function AppRouter() {
    return (
        <Routes>
            <Route path="/login" element={<Login />} />
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
    );
}
