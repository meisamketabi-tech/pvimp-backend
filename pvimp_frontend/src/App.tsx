import ResponsibleHealthOfficerForms from "./pages/ResponsibleHealthOfficerForms";
import ResponsibleHealthDashboard from "./pages/ResponsibleHealthDashboard";
import ResponsibleHealthReports from "./pages/ResponsibleHealthReports";
import ResponsibleHealthKPIDashboard from "./pages/ResponsibleHealthKPIDashboard";
import ResponsibleHealthWorkflow from "./pages/ResponsibleHealthWorkflow";
import ResponsibleHealthSchedule from "./pages/ResponsibleHealthSchedule";
import ResponsibleHealthRiskDashboard from "./pages/ResponsibleHealthRiskDashboard";
import ResponsibleHealthComplaintManagement from "./pages/ResponsibleHealthComplaintManagement";
import ResponsibleHealthTraining from "./pages/ResponsibleHealthTraining";
import ResponsibleHealthApproval from "./pages/ResponsibleHealthApproval";
import ResponsibleHealthChecklist from "./pages/ResponsibleHealthChecklist";
import ResponsibleHealthInspectionResults from "./pages/ResponsibleHealthInspectionResults";
import ResponsibleHealthViolations from "./pages/ResponsibleHealthViolations";
import ResponsibleHealthScoreDashboard from "./pages/ResponsibleHealthScoreDashboard";
import ResponsibleHealthPermits from "./pages/ResponsibleHealthPermits";
import ResponsibleHealthUnits from "./pages/ResponsibleHealthUnits";
import ResponsibleHealthReminders from "./pages/ResponsibleHealthReminders";
import ResponsibleHealthReportsExport from "./pages/ResponsibleHealthReportsExport";
import ResponsibleHealthInspectionRegister from "./pages/ResponsibleHealthInspectionRegister";
import ResponsibleHealthCorrectiveActions from "./pages/ResponsibleHealthCorrectiveActions";
import ResponsibleHealthSampling from "./pages/ResponsibleHealthSampling";
import ResponsibleHealthColdChain from "./pages/ResponsibleHealthColdChain";
import ResponsibleHealthPersonnel from "./pages/ResponsibleHealthPersonnel";
import ResponsibleHealthNotifications from "./pages/ResponsibleHealthNotifications";
import ResponsibleHealthAudit from "./pages/ResponsibleHealthAudit";
import ResponsibleHealthInspectionSchedule from "./pages/ResponsibleHealthInspectionSchedule";
import PublicHealthComplaint from "./pages/PublicHealthComplaint";
import ResponsibleHealthViolationFollowup from "./pages/ResponsibleHealthViolationFollowup";
import ResponsibleHealthAlerts from "./pages/ResponsibleHealthAlerts";

import React from "react";
import AppRouter from "./router/AppRouter";

export default function App(){

    return (
        <AppRouter />
    );

}