import React from "react";
import { useParams } from "react-router-dom";
import DiseaseControlManagementDashboard from "./DiseaseControlManagementDashboard";

export default function DiseaseControlCountyDashboard() {
  const { id } = useParams<{ id: string }>();
  return (
    <DiseaseControlManagementDashboard
      countyCode={id}
      title={`داشبورد اداره مبارزه با بیماری‌های دامی — شهرستان ${id || ""}`}
    />
  );
}
