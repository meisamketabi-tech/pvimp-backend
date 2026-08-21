
import React,{useEffect,useState} from "react";


import {
getChecklists,
getChecklistItems
}
from "../services/checklistService";


import "./Dashboard.css";



export default function ResponsibleHealthChecklist(){


const [lists,setLists]=useState<any[]>([]);

const [items,setItems]=useState<any[]>([]);



useEffect(()=>{


getChecklists()
.then(
r=>setLists(r.data)
);


},[]);



const openChecklist=(id:number)=>{


getChecklistItems(id)
.then(
r=>setItems(r.data)
);


};



return (

<div className="dashboard-container" dir="rtl">


<h1>
چک‌لیست‌های نظارت بهداشتی
</h1>



<div className="dashboard-card">


<h3>
انتخاب چک‌لیست
</h3>



{lists.map(

list=>(

<button

key={list.id}

onClick={()=>
openChecklist(list.id)
}

>

{list.title}

</button>

)

)}



</div>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
شرح مورد
</th>

<th>
الزامی
</th>

</tr>

</thead>



<tbody>


{items.map(

item=>(


<tr key={item.id}>


<td>
{item.item_text}
</td>


<td>
{item.required?
"بله":
"خیر"}
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

