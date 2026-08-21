
import React,{useEffect,useState} from "react";

import {
    getSupervisionInspections
} from "../services/supervisionService";


import {
    SupervisionInspection
} from "../types/SupervisionInspection";



export default function SupervisionViolations(){


const [items,setItems]=useState<SupervisionInspection[]>([]);



useEffect(()=>{

load();

},[]);



async function load(){

const result =
await getSupervisionInspections();

setItems(result);

}



const violations =
items.filter(
item=>(item.violations || []).length>0
);



return (

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
????? ?????
</h1>

</div>



<table className="dashboard-table">


<thead>

<tr>

<th>
????
</th>

<th>
?
</th>

<th>
</th>

<th>
????? ?????
</th>

<th>
????
</th>

</tr>

</thead>



<tbody>


{
violations.map(item=>(

<tr key={item.inspectionId}>


<td>
{item.unitName}
</td>


<td>
{item.city}
</td>


<td>

{
(item.violations || []).join(" - ")
}

</td>


<td>

{
item.judicialReferral
?
"???"
:
"???"
}

</td>


<td>

{
item.sealed
?
"???"
:
"???"
}

</td>


</tr>

))
}



</tbody>


</table>



</div>

)

}



