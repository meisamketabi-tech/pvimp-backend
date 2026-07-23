import React from "react";
import { Routes, Route } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

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
import SupervisionForm from "../pages/SupervisionForm";
import SupervisionGISImport from "../pages/SupervisionGISImport";


export default function AppRouter(){

return (

<Routes>

<Route path="/" element={<MainLayout/>}>


<Route path="supervision" element={<SupervisionDashboard/>}/>

<Route path="supervision/create" element={<SupervisionInspectionCreate/>}/>

<Route path="supervision/list" element={<SupervisionInspectionList/>}/>

<Route path="supervision/reports" element={<SupervisionReports/>}/>

<Route path="supervision/gis" element={<SupervisionGISDashboard/>}/>

<Route path="supervision/violations" element={<SupervisionViolations/>}/>

<Route path="supervision/samples" element={<SupervisionSamples/>}/>

<Route path="supervision/legal" element={<SupervisionLegal/>}/>

<Route path="supervision/settings" element={<SupervisionSettings/>}/>

<Route path="supervision/statistics" element={<SupervisionStatistics/>}/>


<Route path="supervision/national-dashboard" element={<SupervisionNationalDashboard/>}/>

<Route path="supervision/executive-reports" element={<SupervisionExecutiveReports/>}/>

<Route path="supervision/organization-chart" element={<SupervisionOrganizationChart/>}/>

<Route path="supervision/province-view" element={<SupervisionProvinceView/>}/>

<Route path="supervision/county-view" element={<SupervisionCountyView/>}/>


<Route path="supervision/master-reports" element={<SupervisionMasterReports/>}/>

<Route path="supervision/portal" element={<SupervisionPortal/>}/>

<Route path="supervision/trend-analysis" element={<SupervisionTrendAnalysis/>}/>

<Route path="supervision/national-kpis" element={<SupervisionNationalKPIs/>}/>

<Route path="supervision/analytics-center" element={<SupervisionAnalyticsCenter/>}/>

<Route path="supervision/control-room" element={<SupervisionControlRoom/>}/>


<Route path="supervision/ai-analysis" element={<SupervisionAIAnalysis/>}/>

<Route path="supervision/risk-dashboard" element={<SupervisionRiskDashboard/>}/>

<Route path="supervision/operational-dashboard" element={<SupervisionOperationalDashboard/>}/>



<Route
path="county/:id/expert/disease"
element={<DiseaseControlExpertDashboard/>}
/>


<Route
path="county/:id/expert/supervision/create"
element={<SupervisionForm/>}
/>


<Route
path="county/:id/expert/supervision/import"
element={<SupervisionGISImport/>}
/>


</Route>

</Routes>

);

}