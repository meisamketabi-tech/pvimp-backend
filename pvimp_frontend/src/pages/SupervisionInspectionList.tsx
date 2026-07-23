
import React,{useEffect,useState} from "react";

import {
    getSupervisionInspections
} from "../services/supervisionService";


import {
    SupervisionInspection
} from "../types/SupervisionInspection";



export default function SupervisionInspectionList(){


const [items,setItems]=useState<SupervisionInspection[]>([]);



useEffect(()=>{

load();

},[]);



async function load(){

const result = await getSupervisionInspections();

setItems(result);

}



return (

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
???? ?????? ??? ????? ?????
</h1>

</div>



<table className="dashboard-table">


<thead>

<tr>

<th>?????</th>

<th>?????</th>

<th>????</th>

<th>???????</th>

<th>?????</th>

<th>?????</th>

</tr>

</thead>



<tbody>


{
items.map(item=>(

<tr key={item.inspectionId}>


<td>
{item.inspectionId}
</td>


<td>
{item.inspectionDate}
</td>


<td>
{item.unitName}
</td>


<td>
{item.city}
</td>


<td>
{item.inspectorName}
</td>


<td>
{item.inspectionStatus}
</td>


</tr>

))
}



</tbody>


</table>


</div>

)

}
