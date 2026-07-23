import React,{useEffect,useState} from "react";
import "./Dashboard.css";

import { getSupervisionInspections } from "../services/supervisionService";
import { SupervisionInspection } from "../types/SupervisionInspection";


export default function SupervisionDashboard(){

const [data,setData]=useState<SupervisionInspection[]>([]);
const [search,setSearch]=useState("");



useEffect(()=>{

getSupervisionInspections()
.then(result=>setData(result))
.catch(error=>console.error(error));

},[]);



const filteredData=data.filter(item=>

(item.inspectionNumber || "").includes(search) ||
(item.unitName || "").includes(search) ||
(item.inspectorName || "").includes(search)

);



const nonComplianceTotal=data.reduce(
(sum,item)=>sum+(item.nonComplianceCount || 0),
0
);



const completedCount=data.filter(
item=>item.inspectionStatus==="completed"
).length;



const draftCount=data.filter(
item=>item.inspectionStatus==="draft"
).length;



function formatDate(date:string){

return new Date(date).toLocaleDateString("fa-IR");

}



function statusText(status:string){

if(status==="completed")
return "تکمیل شده";

if(status==="draft")
return "پیش نویس";

return status;

}



function yesNo(value:boolean){

return value ? "دارد" : "ندارد";

}



return (

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
داشبورد نظارت بهداشتی
</h1>

<p>
مدیریت و پایش بازرسی های انجام شده
</p>

</div>



<div className="dashboard-cards">


<div className="dashboard-card">
<h3>تعداد بازرسی ها</h3>
<strong>{data.length.toLocaleString("fa-IR")}</strong>
</div>



<div className="dashboard-card">
<h3>موارد عدم انطباق</h3>
<strong>{nonComplianceTotal.toLocaleString("fa-IR")}</strong>
</div>



<div className="dashboard-card">
<h3>بازرسی تکمیل شده</h3>
<strong>{completedCount.toLocaleString("fa-IR")}</strong>
</div>



<div className="dashboard-card">
<h3>پیش نویس</h3>
<strong>{draftCount.toLocaleString("fa-IR")}</strong>
</div>


</div>





<input

type="text"

placeholder="جستجو در شماره، واحد یا بازرس"

value={search}

onChange={(e)=>setSearch(e.target.value)}

className="dashboard-search"

/>





<table className="dashboard-table">


<thead>

<tr>

<th>شماره</th>

<th>تاریخ</th>

<th>واحد</th>

<th>بازرس</th>

<th>وضعیت</th>

<th>عدم انطباق</th>

<th>ارجاع قضایی</th>

<th>نمونه برداری</th>

</tr>

</thead>



<tbody>


{
filteredData.map(item=>(

<tr key={item.inspectionId}>


<td>
{item.inspectionNumber}
</td>



<td>
{formatDate(item.inspectionDate)}
</td>



<td>
{item.unitName}
</td>



<td>
{item.inspectorName}
</td>



<td>
{statusText(item.inspectionStatus || "")}
</td>



<td>
{(item.nonComplianceCount || 0).toLocaleString("fa-IR")}
</td>



<td>
{yesNo(Boolean(item.judicialReferral))}
</td>



<td>
{yesNo(Boolean(item.sampling))}
</td>



</tr>

))
}


</tbody>


</table>


</div>

)

}