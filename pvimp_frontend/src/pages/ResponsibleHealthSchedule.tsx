
import React,{useEffect,useState} from "react";

import {
getSchedule,
completeSchedule
}
from "../services/scheduleService";


import "./Dashboard.css";



export default function ResponsibleHealthSchedule(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getSchedule(1)
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
برنامه بازدید مسئول بهداشتی
</h1>



<div className="dashboard-card">


<table>

<thead>

<tr>

<th>
واحد
</th>

<th>
نوع بازدید
</th>

<th>
تاریخ
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
{item.inspection_type}
</td>


<td>
{item.scheduled_date}
</td>


<td>
{item.completed?
"انجام شده":
"در انتظار"}
</td>


<td>

<button
onClick={()=>
completeSchedule(item.id)
.then(load)
}
>
تکمیل
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

