
import React,{useEffect,useState} from "react";

import {
getTrainings
}
from "../services/trainingService";

import "./Dashboard.css";



export default function ResponsibleHealthTraining(){

const [items,setItems]=useState<any[]>([]);

useEffect(()=>{

getTrainings()
.then(
r=>setItems(r.data)
);

},[]);



return(

<div className="dashboard-container" dir="rtl">

<h1>
مدیریت آموزش‌های بهداشتی
</h1>

<div className="dashboard-card">

<table>

<thead>

<tr>

<th>عنوان</th>
<th>گروه هدف</th>
<th>مدرس</th>
<th>تاریخ</th>
<th>محل</th>

</tr>

</thead>

<tbody>

{items.map(item=>(

<tr key={item.id}>

<td>{item.title}</td>
<td>{item.target_group}</td>
<td>{item.instructor}</td>
<td>{item.training_date}</td>
<td>{item.location}</td>

</tr>

))}

</tbody>

</table>

</div>

</div>

)

}
