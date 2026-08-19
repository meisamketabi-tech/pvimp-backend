
import React,{useEffect,useState} from "react";


import {
getViolations
}
from "../services/violationService";


import "./Dashboard.css";



export default function ResponsibleHealthViolations(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getViolations()
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
مدیریت تخلفات بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
نوع تخلف
</th>

<th>
مستند قانونی
</th>

<th>
شرح
</th>

<th>
شدت
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
{item.violation_type}
</td>


<td>
{item.legal_reference}
</td>


<td>
{item.description}
</td>


<td>
{item.severity}
</td>


<td>
{item.resolved?
"رفع شده":
"باز"}
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

