
import React,{useEffect,useState} from "react";


import {
getNotifications,
markNotificationRead
}
from "../services/notificationService";


import "./Dashboard.css";



export default function ResponsibleHealthNotifications(){


const [items,setItems]=useState<any[]>([]);



const load=()=>{

getNotifications(1)
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
اعلان‌ها و هشدارهای بهداشتی
</h1>



<div className="dashboard-card">


<table>


<thead>

<tr>

<th>
عنوان
</th>

<th>
پیام
</th>

<th>
نوع
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
{item.title}
</td>


<td>
{item.message}
</td>


<td>
{item.notification_type}
</td>


<td>
{item.is_read?
"خوانده شده":
"جدید"}
</td>


<td>


<button

onClick={()=>
markNotificationRead(item.id)
.then(load)
}

>
خواندم
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

