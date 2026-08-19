
import React,{useEffect,useState} from "react";


import {
getPersonnel
}
from "../services/personnelService";


import "./Dashboard.css";



export default function ResponsibleHealthPersonnel(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getPersonnel()
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
مدیریت کارکنان و مسئولین بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
نام
</th>

<th>
سمت
</th>

<th>
شماره مجوز
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
{item.full_name}
</td>


<td>
{item.position}
</td>


<td>
{item.license_number}
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

