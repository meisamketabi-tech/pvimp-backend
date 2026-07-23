
import React,{useEffect,useState} from "react";


import {
getInspectionSchedule,
completeInspectionSchedule
}
from "../services/inspectionScheduleService";


import "./Dashboard.css";



export default function ResponsibleHealthInspectionSchedule(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getInspectionSchedule(1)
.then(
r=>setItems(r.data)
);

};



useEffect(()=>{

load();

},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
برنامه بازدیدهای بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
واحد
</th>

<th>
تاریخ برنامه
</th>

<th>
نوع بازدید
</th>

<th>
وضعیت
</th>

<th>
عملیات
</th>

</tr>

</thead>



<tbody>


{items.map(

item=>(


<tr key={item.id}>


<td>
{item.unit_name}
</td>


<td>
{item.scheduled_date}
</td>


<td>
{item.inspection_type}
</td>


<td>
{item.completed?
"انجام شده":
"برنامه‌ریزی شده"}
</td>


<td>

<button

onClick={()=>
completeInspectionSchedule(item.id)
.then(load)
}

>
ثبت انجام بازدید
</button>

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
