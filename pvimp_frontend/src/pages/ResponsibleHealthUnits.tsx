
import React,{useEffect,useState} from "react";


import {
getHealthUnits
}
from "../services/healthUnitService";


import "./Dashboard.css";



export default function ResponsibleHealthUnits(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getHealthUnits()
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
مراکز تحت مسئولیت بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
نام مرکز
</th>

<th>
نوع مرکز
</th>

<th>
مسئول
</th>

<th>
تلفن
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
{item.name}
</td>


<td>
{item.unit_type}
</td>


<td>
{item.owner_name}
</td>


<td>
{item.phone}
</td>


<td>
{item.active?
"فعال":
"غیرفعال"}
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
