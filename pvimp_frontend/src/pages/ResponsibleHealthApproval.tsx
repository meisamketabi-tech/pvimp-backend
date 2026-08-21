
import React,{useEffect,useState} from "react";


import {
getApprovalRequests,
reviewApproval
}
from "../services/approvalService";


import "./Dashboard.css";



export default function ResponsibleHealthApproval(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getApprovalRequests()
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
تایید و گردش درخواست‌ها
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
نوع درخواست
</th>

<th>
شناسه
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
{item.entity_type}
</td>


<td>
{item.entity_id}
</td>


<td>
{item.status}
</td>


<td>

<button

onClick={()=>
reviewApproval(
item.id,
"تایید شده"
)
.then(load)
}

>
تایید
</button>


<button

onClick={()=>
reviewApproval(
item.id,
"رد شده"
)
.then(load)
}

>
رد
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

