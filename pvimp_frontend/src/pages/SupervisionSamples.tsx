
import React,{useEffect,useState} from "react";
import {getSupervisionInspections} from "../services/supervisionService";
import {SupervisionInspection} from "../types/SupervisionInspection";

export default function SupervisionSamples(){

const [data,setData]=useState<SupervisionInspection[]>([]);

useEffect(()=>{
getSupervisionInspections().then(setData);
},[]);


const samples=data.filter(x=>x.sampling);


return(
<div className="dashboard-container" dir="rtl">

<div className="expert-header">
<h1>Samples</h1>
</div>

<table className="dashboard-table">

<thead>
<tr>
<th>????</th>
<th>??? ?????</th>
<th>?????</th>
<th>?????</th>
</tr>
</thead>

<tbody>

{
samples.map(item=>(

<tr key={item.inspectionId}>

<td>{item.unitName}</td>

<td>{item.sampleType}</td>

<td>{item.sampleCount}</td>

<td>{item.inspectorName}</td>

</tr>

))
}

</tbody>

</table>

</div>
)

}



