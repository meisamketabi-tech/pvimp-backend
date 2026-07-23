
import React,{useEffect,useState} from "react";

import {
getNotifications,
markRead
}
from "../../services/notificationService";


export default function NotificationBell(){


const [items,setItems]=useState<any[]>([]);



useEffect(()=>{

getNotifications(1)
.then(
r=>setItems(r.data)
);

},[]);



return (

<div
dir="rtl"
>

<button>

🔔

{items.filter(
x=>!x.is_read
).length}

</button>


<div>


{items.map(
item=>(

<div
key={item.id}
onClick={()=>markRead(item.id)}
>

<strong>
{item.title}
</strong>

<p>
{item.message}
</p>


</div>

)

)}


</div>


</div>

)

}
