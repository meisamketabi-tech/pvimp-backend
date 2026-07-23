
import React,{useEffect,useState} from "react";

import {
getTasks,
updateTaskStatus
}
from "../services/workflowService";


import "./Dashboard.css";



export default function ResponsibleHealthWorkflow(){


const [tasks,setTasks]=useState<any[]>([]);



const load=()=>{

getTasks()
.then(
r=>setTasks(r.data)
);

};



useEffect(()=>{

load();

},[]);



const changeStatus=(
id:number,
status:string
)=>{

updateTaskStatus(
id,
status
)
.then(
load
);

};



return (

<div className="dashboard-container" dir="rtl">


<h1>
گردش کار مسئول بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
شناسه
</th>

<th>
نوع عملیات
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


{tasks.map(
task=>(


<tr key={task.id}>


<td>
{task.id}
</td>


<td>
{task.entity_type}
</td>


<td>
{task.current_status}
</td>



<td>

<button
onClick={()=>changeStatus(
task.id,
"بررسی شده"
)}
>
تایید
</button>


<button
onClick={()=>changeStatus(
task.id,
"نیازمند اصلاح"
)}
>
برگشت
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
