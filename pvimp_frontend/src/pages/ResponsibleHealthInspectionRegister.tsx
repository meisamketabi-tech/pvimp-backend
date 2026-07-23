
import React,{useEffect,useState} from "react";


import {
getInspections
}
from "../services/inspectionService";


import "./Dashboard.css";



export default function ResponsibleHealthInspectionRegister(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getInspections()
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
ثبت و مدیریت بازدیدهای بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
واحد
</th>

<th>
تاریخ بازدید
</th>

<th>
نوع بازدید
</th>

<th>
نتیجه
</th>

<th>
شرح
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
{item.inspection_date}
</td>


<td>
{item.inspection_type}
</td>


<td>
{item.result}
</td>


<td>
{item.description}
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
