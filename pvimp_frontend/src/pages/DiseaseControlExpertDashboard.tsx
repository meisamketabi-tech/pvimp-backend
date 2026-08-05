import React,{useEffect,useState} from "react";
import {useNavigate,useParams} from "react-router-dom";
import {getCountyName} from "../utils/counties";
import "./Dashboard.css";

import {
ResponsiveContainer,
BarChart,
Bar,
XAxis,
YAxis,
Tooltip,
CartesianGrid
} from "recharts";


export default function DiseaseControlExpertDashboard(){


const navigate=useNavigate();

const {id}=useParams();

const county=getCountyName(id);



const [diseaseData,setDiseaseData]=useState<any[]>([]);
const [vaccination,setVaccination]=useState<any[]>([]);
const [surveillance,setSurveillance]=useState<any[]>([]);
const [lastImport,setLastImport]=useState<any[]>([]);



useEffect(()=>{


fetch("http://localhost:8000/gis-dashboard/disease-summary")
.then(r=>r.json())
.then(setDiseaseData)
.catch(()=>{});



fetch("http://localhost:8000/gis-dashboard/vaccination-summary")
.then(r=>r.json())
.then(setVaccination)
.catch(()=>{});



fetch("http://localhost:8000/gis-dashboard/surveillance-summary")
.then(r=>r.json())
.then(setSurveillance)
.catch(()=>{});



fetch("http://localhost:8000/gis-dashboard/last-import")
.then(r=>r.json())
.then(setLastImport)
.catch(()=>{});


},[]);




return(

<div className="dashboard-container" dir="rtl">


<div className="expert-header">

<h1>
داشبورد کارشناس بهداشت و مدیریت بیماری‌های دامی
</h1>

<p>
شهرستان {county}
</p>

</div>




<div className="cards">


<div className="card">

<h3>
آخرین فایل GIS
</h3>

<strong>
{
lastImport.length>0
?
lastImport[0].file
:
"عدم دریافت"
}
</strong>

<p>
{
lastImport.length>0
?
lastImport[0].date
:
""
}
</p>

</div>




<div className="card">

<h3>
کانون‌های بیماری
</h3>

<strong>
{
diseaseData.reduce(
(a,b)=>a+b.count,
0
)
}
</strong>

</div>




<div className="card">

<h3>
عملیات مراقبت
</h3>

<strong>
{
surveillance.reduce(
(a,b)=>a+b.count,
0
)
}
</strong>

</div>




<div className="card">

<h3>
رکورد واکسیناسیون
</h3>

<strong>
{
vaccination.reduce(
(a,b)=>a+b.count,
0
)
}
</strong>

</div>


</div>






<div className="dashboard-grid">



<div className="panel chart-panel">

<h2>
بیماری‌های ثبت شده GIS
</h2>


<ResponsiveContainer width="100%" height={300}>

<BarChart data={diseaseData}>


<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="disease"/>

<YAxis/>

<Tooltip/>

<Bar
dataKey="count"
fill="#008577"
/>


</BarChart>

</ResponsiveContainer>


</div>






<div className="panel">


<h2>
آخرین عملیات GIS
</h2>


<ul className="action-list">

{

lastImport.map(
(item,index)=>(

<li key={index}>

{item.file}
-
{item.status}

</li>

)

)

}


</ul>


</div>






<div className="panel upload-panel">


<h2>
ورود اطلاعات GIS
</h2>


<p>
آپلود فایل‌های خروجی سامانه GIS توسط کارشناس GIS اداره کل
</p>



<button

className="upload-btn"

onClick={()=>navigate(
`/county/${id}/expert/disease/import`
)}

>

مشاهده و دریافت اطلاعات

</button>


</div>





</div>



</div>

)

}