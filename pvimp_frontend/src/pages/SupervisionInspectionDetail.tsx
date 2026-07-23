import React,{useEffect,useState} from "react";
import { useParams } from "react-router-dom";
import "./Dashboard.css";


export default function SupervisionInspectionDetail(){

const {id}=useParams();

const [data,setData]=useState<any>(null);



useEffect(()=>{

fetch(
`http://localhost:8000/api/v1/inspection/${id}`
)

.then(res=>res.json())

.then(result=>setData(result))

.catch(err=>console.error(err));


},[id]);



if(!data){

return (

<div className="dashboard-container" dir="rtl">

<h2>
در حال دریافت اطلاعات بازرسی...
</h2>

</div>

)

}



return (

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
جزئیات بازرسی
</h1>

<p>
شماره بازرسی: {data.inspectionNumber}
</p>

</div>



<div className="dashboard-cards">


<div className="dashboard-card">

<h3>
واحد
</h3>

<strong>
{data.unitName}
</strong>

</div>



<div className="dashboard-card">

<h3>
بازرس
</h3>

<strong>
{data.inspectorName}
</strong>

</div>



<div className="dashboard-card">

<h3>
وضعیت
</h3>

<strong>
{data.status}
</strong>

</div>



</div>



<table className="dashboard-table">

<thead>

<tr>

<th>
شرح
</th>

<th>
مقدار
</th>

</tr>

</thead>


<tbody>

<tr>

<td>
تاریخ بازرسی
</td>

<td>
{data.inspectionDate}
</td>

</tr>


<tr>

<td>
عدم انطباق
</td>

<td>
{data.nonComplianceCount}
</td>

</tr>


<tr>

<td>
ارجاع قضایی
</td>

<td>
{data.judicialReferral ? "دارد":"ندارد"}
</td>

</tr>


<tr>

<td>
نمونه برداری
</td>

<td>
{data.sampling ? "دارد":"ندارد"}
</td>

</tr>


</tbody>


</table>


</div>

)

}