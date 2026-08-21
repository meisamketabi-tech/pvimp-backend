
import React,{useEffect,useState} from "react";


import {
getColdChainLogs,
getColdChainAlerts
}
from "../services/coldChainService";


import "./Dashboard.css";



export default function ResponsibleHealthColdChain(){


const [items,setItems]=useState<any[]>([]);

const [alerts,setAlerts]=useState<any[]>([]);



useEffect(()=>{


getColdChainLogs()
.then(
r=>setItems(r.data)
);



getColdChainAlerts()
.then(
r=>setAlerts(r.data)
);



},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
پایش زنجیره سرد و تجهیزات
</h1>



<div className="dashboard-grid">


<div className="dashboard-card">

<h3>
کل ثبت‌ها
</h3>

<h2>
{items.length}
</h2>

</div>



<div className="dashboard-card">

<h3>
هشدارها
</h3>

<h2>
{alerts.length}
</h2>

</div>


</div>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
تجهیز
</th>

<th>
دما
</th>

<th>
حداقل
</th>

<th>
حداکثر
</th>

<th>
وضعیت
</th>

</tr>

</thead>



<tbody>


{items.map(

item=>(


<tr key={item.id}>


<td>
{item.equipment_name}
</td>


<td>
{item.temperature}
</td>


<td>
{item.min_temperature}
</td>


<td>
{item.max_temperature}
</td>


<td>
{item.status}
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

