
import React,{useEffect,useState} from "react";


import {
getReminders,
completeReminder
}
from "../services/reminderService";


import "./Dashboard.css";



export default function ResponsibleHealthReminders(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getReminders()
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
یادآوری‌های مسئول بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
عنوان
</th>

<th>
نوع مورد
</th>

<th>
تاریخ سررسید
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
{item.title}
</td>


<td>
{item.entity_type}
</td>


<td>
{item.due_date}
</td>


<td>

<button

onClick={()=>
completeReminder(item.id)
.then(load)
}

>
انجام شد
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
