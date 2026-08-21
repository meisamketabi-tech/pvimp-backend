
import React,{useEffect,useState} from "react";

import {
getOfficerDashboard
}
from "../services/responsibleHealthService";


import "./Dashboard.css";



export default function ResponsibleHealthDashboard(){


const [data,setData]=useState<any>({});



useEffect(()=>{


getOfficerDashboard(1)
.then(res=>{

setData(res.data);

});


},[]);




return (

<div className="dashboard-container" dir="rtl">


<h1>
داشبورد مسئول بهداشتی
</h1>


<div className="dashboard-grid">


<div className="dashboard-card">

<h3>
تعداد بازدیدها
</h3>

<strong>
{data.inspections || 0}
</strong>

</div>



<div className="dashboard-card">

<h3>
عدم انطباق‌ها
</h3>

<strong>
{data.nonconformities || 0}
</strong>


</div>



<div className="dashboard-card">

<h3>
وضعیت فعالیت
</h3>

<strong>
{data.status}
</strong>

</div>


</div>


</div>

)

}

