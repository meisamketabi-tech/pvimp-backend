
import React,{useEffect,useState} from "react";


import {
getPermits
}
from "../services/permitService";


import "./Dashboard.css";



export default function ResponsibleHealthPermits(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getPermits()
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
مدیریت مجوزهای بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
شماره مجوز
</th>

<th>
نوع مجوز
</th>

<th>
تاریخ صدور
</th>

<th>
تاریخ انقضا
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
{item.permit_number}
</td>


<td>
{item.permit_type}
</td>


<td>
{item.issue_date}
</td>


<td>
{item.expire_date}
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

