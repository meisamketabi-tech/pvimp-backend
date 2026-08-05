
import React,{useEffect,useState} from "react";
import {getSupervisionInspections} from "../services/supervisionService";
import {SupervisionInspection} from "../types/SupervisionInspection";


export default function SupervisionDashboardAdvanced(){

const [data,setData]=useState<SupervisionInspection[]>([]);


useEffect(()=>{

getSupervisionInspections().then(setData);

},[]);



return(

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
??????? ??????? ??????? ????? ?????
</h1>

</div>


<div className="dashboard-cards">


<div className="dashboard-card">
<h3>?????? ?????</h3>
<strong>{data.length}</strong>
</div>


<div className="dashboard-card">
<h3>??????? ??????</h3>
<strong>
{
data.filter(x=>(x.nonComplianceCount || 0)>2).length
}
</strong>
</div>


<div className="dashboard-card">
<h3>????? ??????</h3>
<strong>
{
data.filter(x=>x.judicialReferral).length
}
</strong>
</div>


</div>


</div>

)

}
