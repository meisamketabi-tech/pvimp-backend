
import React,{useEffect,useState} from "react";


import {
getComplaints,
updateComplaint
}
from "../services/complaintService";


import "./Dashboard.css";



export default function ResponsibleHealthComplaintManagement(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getComplaints()
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
مدیریت شکایات بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
واحد
</th>

<th>
موضوع
</th>

<th>
شرح
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
{item.unit_name}
</td>


<td>
{item.subject}
</td>


<td>
{item.description}
</td>


<td>
{item.status}
</td>



<td>

<button

onClick={()=>updateComplaint(
item.id,
"در حال بررسی"
)
.then(load)}

>
بررسی
</button>



<button

onClick={()=>updateComplaint(
item.id,
"مختومه"
)
.then(load)}

>
مختومه
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
