import SupervisionImport from "../pages/SupervisionImport";
import React from "react";
import { Routes, Route } from "react-router-dom";
import SupervisionForm from "../pages/SupervisionForm";
import SupervisionDashboard from "../pages/SupervisionDashboard";
import MainLayout from "../layouts/MainLayout";
import ProtectedRoute from "../routes/ProtectedRoute";

import Login from "../pages/Login";

import DashboardAdmin from "../pages/DashboardAdmin";
import KPIAnalysis from "../pages/KPIAnalysis";
import KpiDetail from "../pages/KpiDetail";

import HealthDeputyDashboard from "../pages/HealthDeputyDashboard";

import DiseaseControlManager from "../pages/DiseaseControlManager";

import DiseaseControlExpertDashboard from "../pages/DiseaseControlExpertDashboard";
import QuarantineExpertDashboard from "../pages/QuarantineExpertDashboard";
import SupervisionExpertDashboard from "../pages/SupervisionExpertDashboard";
import PoultryExpertDashboard from "../pages/PoultryExpertDashboard";
import DiagnosisExpertDashboard from "../pages/DiagnosisExpertDashboard";
import LabExpertDashboard from "../pages/LabExpertDashboard";

import ExcelImport from "../pages/ExcelImport";
import SupervisionImport from "../pages/SupervisionImport";

import CountyList from "../pages/CountyList";
import CountyDashboard from "../pages/CountyDashboard";



export default function App(){


return(


<Routes>



<Route

path="/login"

element={<Login />}

/>





<Route

path="/"

element={

<ProtectedRoute>

<MainLayout />

</ProtectedRoute>

}

>



<Route

index

element={<DashboardAdmin />}

/>





<Route

path="dashboard"

element={<DashboardAdmin />}

/>





<Route

path="health-deputy"

element={<HealthDeputyDashboard />}

/>





<Route

path="disease-control"

element={<DiseaseControlManager />}

/>





<Route

path="counties"

element={<CountyList />}

/>





<Route

path="county/:id"

element={<CountyDashboard />}

/>





<Route

path="county/:id/expert/disease"

element={<DiseaseControlExpertDashboard />}

/>





<Route

path="county/:id/expert/quarantine"

element={<QuarantineExpertDashboard />}

/>





<Route

path="county/:id/expert/supervision"

element={<SupervisionExpertDashboard />}

/>





<Route

path="county/:id/expert/poultry"

element={<PoultryExpertDashboard />}

/>





<Route

path="county/:id/expert/diagnosis"

element={<DiagnosisExpertDashboard />}

/>





<Route

path="county/:id/expert/laboratory"

element={<LabExpertDashboard />}

/>





<Route

path="supervision"

element={<SupervisionDashboard />}

/>


<Route

path="supervision-import"

element={<SupervisionImport />}

/>





<Route

path="excel-import"

element={<ExcelImport />}

/>





<Route

path="county/:id/expert/disease/import"

element={<ExcelImport />}

/>





<Route

path="kpi"

element={<KPIAnalysis />}

/>





<Route

path="kpi/:id"

element={<KpiDetail />}

/>


<Route
path="county/:id/expert/supervision/form"
element={<SupervisionForm />}
/>


<Route
path="poultry"
element={<PoultryExpertDashboard />}
/>


<Route
path="county/:id/expert/supervision/import"
element={<SupervisionImport />}
/>



<Route
path="county/:id/expert/supervision/create"
element={<SupervisionForm />}
/>


</Route>



</Routes>


)

}