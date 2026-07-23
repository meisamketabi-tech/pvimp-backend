
import React,{useEffect,useState} from "react";


import {
getReports,
createReport
}
from "../services/reportService";


import "./Dashboard.css";



export default function ResponsibleHealthReportsExport(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getReports()
.then(
r=>setItems(r.data)
);

};



useEffect(()=>{

load();

},[]);



const create=()=>{

createReport({

report_type:"health",

title:"گزارش مسئول بهداشتی",

parameters:"{}",

created_by:1

})
.then(load);

};



return (

<div className="dashboard-container" dir="rtl">


<h1>
مدیریت گزارش‌ها
</h1>



<div className="dashboard-card">


<button
onClick={create}
>
ایجاد گزارش جدید
</button>



<table>


<thead>

<tr>

<th>
عنوان
</th>

<th>
نوع گزارش
</th>

<th>
تاریخ ایجاد
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
{item.report_type}
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
