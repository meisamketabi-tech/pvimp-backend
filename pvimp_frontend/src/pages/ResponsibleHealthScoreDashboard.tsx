
import React,{useEffect,useState} from "react";


import {
getScores
}
from "../services/scoreService";


import "./Dashboard.css";



export default function ResponsibleHealthScoreDashboard(){


const [scores,setScores]=useState<any[]>([]);



useEffect(()=>{


getScores()
.then(
r=>setScores(r.data)
);



},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
رتبه‌بندی عملکرد بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
واحد
</th>

<th>
امتیاز بازرسی
</th>

<th>
امتیاز انطباق
</th>

<th>
امتیاز نهایی
</th>

<th>
رتبه
</th>

</tr>

</thead>



<tbody>


{scores.map(

item=>(


<tr key={item.id}>


<td>
{item.unit_name}
</td>


<td>
{item.inspection_score}
</td>


<td>
{item.compliance_score}
</td>


<td>
{item.final_score}
</td>


<td>
{item.grade}
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

