
import React,{useEffect,useState} from "react";


import {
getActions,
completeAction
}
from "../services/actionPlanService";


import "./Dashboard.css";



export default function ResponsibleHealthCorrectiveActions(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getActions()
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
پیگیری اقدامات اصلاحی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
مسئول اقدام
</th>

<th>
شرح اقدام
</th>

<th>
تاریخ سررسید
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
{item.responsible_person}
</td>


<td>
{item.action_description}
</td>


<td>
{item.due_date}
</td>


<td>
{item.status}
</td>


<td>

<button

onClick={()=>
completeAction(item.id)
.then(load)
}

>
تکمیل اقدام
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
