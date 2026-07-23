
import React,{useEffect,useState} from "react";


import {
getHealthAlerts,
updateHealthAlert
}
from "../services/healthAlertService";


import "./Dashboard.css";



export default function ResponsibleHealthAlerts(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getHealthAlerts()
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
مدیریت هشدارهای بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
نوع هشدار
</th>

<th>
عنوان
</th>

<th>
شدت
</th>

<th>
منبع
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
{item.alert_type}
</td>


<td>
{item.title}
</td>


<td>
{item.severity}
</td>


<td>
{item.source}
</td>


<td>
{item.status}
</td>


<td>

<button

onClick={()=>
updateHealthAlert(
item.id,
"بررسی شده"
)
.then(load)
}

>
بررسی
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
