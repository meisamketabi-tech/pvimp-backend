
import React,{useEffect,useState} from "react";
import {getSupervisionInspections} from "../services/supervisionService";
import {SupervisionInspection} from "../types/SupervisionInspection";


export default function SupervisionLegal(){

const [data,setData]=useState<SupervisionInspection[]>([]);


useEffect(()=>{
getSupervisionInspections().then(setData);
},[]);



const items=data.filter(
x=>x.judicialReferral
);



return(

<div className="dashboard-container" dir="rtl">

<div className="expert-header">
<h1>?????? ??? ????? ?????</h1>
</div>


<table className="dashboard-table">

<thead>
<tr>
<th>????</th>
<th>???</th>
<th>???</th>
</tr>
</thead>


<tbody>

{
items.map(x=>(

<tr key={x.inspectionId}>

<td>{x.unitName}</td>

<td>{x.city}</td>

<td>{x.description}</td>

</tr>

))
}

</tbody>

</table>


</div>

)

}
