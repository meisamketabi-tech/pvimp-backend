
import React,{useEffect,useState} from "react";


import {
getAuditLogs
}
from "../services/auditService";


import "./Dashboard.css";



export default function ResponsibleHealthAudit(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getAuditLogs()
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
سوابق فعالیت و ثبت تغییرات
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
کاربر
</th>

<th>
عملیات
</th>

<th>
نوع موجودیت
</th>

<th>
شناسه
</th>

<th>
شرح
</th>

<th>
تاریخ
</th>

</tr>

</thead>



<tbody>


{items.map(

item=>(


<tr key={item.id}>


<td>
{item.user_id}
</td>


<td>
{item.action}
</td>


<td>
{item.entity_type}
</td>


<td>
{item.entity_id}
</td>


<td>
{item.description}
</td>


<td>
{item.created_at}
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
