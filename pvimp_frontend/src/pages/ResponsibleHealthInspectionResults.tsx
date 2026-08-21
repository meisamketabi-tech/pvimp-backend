
import React,{useEffect,useState} from "react";


import {
getInspectionResults
}
from "../services/inspectionResultService";


import "./Dashboard.css";



export default function ResponsibleHealthInspectionResults(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getInspectionResults(1)
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
نتایج ارزیابی بازدیدهای بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
امتیاز
</th>

<th>
نتیجه
</th>

<th>
یافته‌ها
</th>

<th>
تاریخ بازدید
</th>

</tr>

</thead>



<tbody>


{items.map(

item=>(


<tr key={item.id}>


<td>
{item.score}
</td>


<td>
{item.result}
</td>


<td>
{item.findings}
</td>


<td>
{item.inspection_date}
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

