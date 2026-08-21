
import React,{useEffect,useState} from "react";


import {
getSamples
}
from "../services/samplingService";


import "./Dashboard.css";



export default function ResponsibleHealthSampling(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getSamples()
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
مدیریت نمونه‌برداری بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
کد نمونه
</th>

<th>
نوع نمونه
</th>

<th>
آزمایشگاه
</th>

<th>
تاریخ نمونه‌برداری
</th>

<th>
نتیجه
</th>

</tr>

</thead>



<tbody>


{items.map(

item=>(


<tr key={item.id}>


<td>
{item.sample_code}
</td>


<td>
{item.sample_type}
</td>


<td>
{item.laboratory}
</td>


<td>
{item.sampling_date}
</td>


<td>
{item.result}
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

