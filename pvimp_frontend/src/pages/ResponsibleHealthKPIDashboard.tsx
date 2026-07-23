
import React,{useEffect,useState} from "react";

import {
getStatistics,
getComplianceScore,
getOfficerSummary
}
from "../services/responsibleHealthService";


import "./Dashboard.css";



export default function ResponsibleHealthKPIDashboard(){


const [stats,setStats]=useState<any>({});

const [score,setScore]=useState<any>({});

const [summary,setSummary]=useState<any>({});



useEffect(()=>{


getStatistics()
.then(
r=>setStats(r.data)
);



getComplianceScore(1)
.then(
r=>setScore(r.data)
);



getOfficerSummary(1)
.then(
r=>setSummary(r.data)
);



},[]);




return (

<div className="dashboard-container" dir="rtl">


<h1>
داشبورد شاخص‌های مسئول بهداشتی
</h1>



<div className="dashboard-grid">


<div className="dashboard-card">

<h3>
تعداد مسئولین
</h3>

<strong>
{stats.officers || 0}
</strong>

</div>



<div className="dashboard-card">

<h3>
بازدیدها
</h3>

<strong>
{stats.inspections || 0}
</strong>

</div>



<div className="dashboard-card">

<h3>
عدم انطباق
</h3>

<strong>
{stats.nonconformities || 0}
</strong>

</div>



<div className="dashboard-card">

<h3>
امتیاز انطباق
</h3>

<strong>
{score.compliance_score || 0}%
</strong>

</div>



<div className="dashboard-card">

<h3>
بازدید مسئول انتخابی
</h3>

<strong>
{summary.inspections || 0}
</strong>

</div>


</div>


</div>

)

}
