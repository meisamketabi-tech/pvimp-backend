
import React,{useEffect,useState} from "react";


import {
getRisks,
getHighRisks
}
from "../services/riskService";


import "./Dashboard.css";



export default function ResponsibleHealthRiskDashboard(){


const [risks,setRisks]=useState<any[]>([]);

const [high,setHigh]=useState<any[]>([]);



useEffect(()=>{


getRisks()
.then(
r=>setRisks(r.data)
);



getHighRisks()
.then(
r=>setHigh(r.data)
);



},[]);




return (

<div className="dashboard-container" dir="rtl">


<h1>
ارزیابی ریسک واحدهای تحت نظارت
</h1>



<div className="dashboard-grid">


<div className="dashboard-card">

<h3>
کل ارزیابی‌ها
</h3>

<h2>
{risks.length}
</h2>

</div>



<div className="dashboard-card">

<h3>
ریسک بحرانی
</h3>

<h2>
{high.length}
</h2>

</div>


</div>



<div className="dashboard-card">


<table>

<thead>

<tr>

<th>
واحد
</th>

<th>
سطح ریسک
</th>

<th>
امتیاز
</th>

<th>
توضیحات
</th>

</tr>

</thead>


<tbody>


{risks.map(
item=>(

<tr key={item.id}>

<td>
{item.unit_name}
</td>

<td>
{item.risk_level}
</td>

<td>
{item.risk_score}
</td>

<td>
{item.description}
</td>

</tr>

)

)}


</tbody>


</table>


</div>


</div>

)

}
