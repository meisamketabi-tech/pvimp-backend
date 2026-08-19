
import React,{useEffect,useState} from "react";

import {
    getSupervisionInspections
} from "../services/supervisionService";


import {
    SupervisionInspection
} from "../types/SupervisionInspection";



export default function SupervisionReports(){


const [data,setData]=useState<SupervisionInspection[]>([]);



useEffect(()=>{

load();

},[]);



async function load(){

const result =
await getSupervisionInspections();

setData(result);

}



const total =
data.length;


const violations =
data.reduce(
(sum,item)=>sum+(item.nonComplianceCount || 0),
0
);



const samples =
data.reduce(
(sum,item)=>sum+(item.sampleCount || 0),
0
);



const destroyed =
data.reduce(
(sum,item)=>sum+(item.destroyedProductKg || 0),
0
);



return (

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
????? ??? ? ????? ?????
</h1>

</div>



<div className="dashboard-cards">


<div className="dashboard-card">

<h3>
????? ?? </h3>

<strong>
{total}
</strong>

</div>



<div className="dashboard-card">

<h3>
?? </h3>

<strong>
{violations}
</strong>

</div>



<div className="dashboard-card">

<h3>
????? ????? ??
</h3>

<strong>
{samples}
</strong>

</div>



<div className="dashboard-card">

<h3>
????? ???? (?)
</h3>

<strong>
{destroyed}
</strong>

</div>



</div>


</div>

)

}



