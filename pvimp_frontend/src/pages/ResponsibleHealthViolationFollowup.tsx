
import React,{useEffect,useState} from "react";


import {
getViolationFollowups
}
from "../services/violationFollowupService";


import "./Dashboard.css";



export default function ResponsibleHealthViolationFollowup(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getViolationFollowups(1)
.then(
r=>setItems(r.data)
);


},[]);



return (

<div className="dashboard-container" dir="rtl">


<h1>
پیگیری تخلفات و اقدامات نظارتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
تاریخ پیگیری
</th>

<th>
نتیجه
</th>

<th>
شرح
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
{item.followup_date}
</td>


<td>
{item.result}
</td>


<td>
{item.description}
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

