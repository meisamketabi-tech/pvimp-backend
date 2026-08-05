import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUserDetails, UserDetails } from "../services/userService";

import {
 ResponsiveContainer,
 BarChart,
 Bar,
 XAxis,
 YAxis,
 Tooltip,
 CartesianGrid,
 LineChart,
 Line,
 PieChart,
 Pie,
 Cell
} from "recharts";

import "./Dashboard.css";


const kpis = [
 {
  title:"پوشش واکسیناسیون",
  value:"92%",
  icon:"💉",
  detail:"درصد تحقق برنامه واکسیناسیون استان",
  path:"/county/1/expert/disease"
 },
 {
  title:"بهداشت عمومی",
  value:"87%",
  icon:"🥩",
  detail:"عملکرد نظارت بر مواد خام دامی",
  path:"/health-deputy"
 },
 {
  title:"گواهی قرنطینه",
  value:"4210",
  icon:"🚧",
  detail:"گواهی صادر شده در سال جاری",
  path:"/county/1/expert/quarantine"
 },
 {
  title:"نمونه‌های آزمایشگاهی",
  value:"28600",
  icon:"🔬",
  detail:"نمونه بررسی شده توسط آزمایشگاه",
  path:"/county/1/expert/laboratory"
 },
 {
  title:"عملکرد طیور",
  value:"89%",
  icon:"🐔",
  detail:"شاخص عملکرد اداره طیور",
  path:"/poultry"
 },
 {
  title:"هشدارهای مدیریتی",
  value:"18",
  icon:"⚠️",
  detail:"موارد نیازمند اقدام مدیر",
  path:"/kpi"
 }
];

const departmentData=[
 {
  name:"مبارزه با بیماری‌ها",
  value:95
 },
 {
  name:"بهداشت عمومی",
  value:87
 },
 {
  name:"قرنطینه",
  value:92
 },
 {
  name:"آزمایشگاه",
  value:94
 },
 {
  name:"طیور",
  value:89
 }
];


const vaccinationTrend=[
 {
  month:"فروردین",
  value:72
 },
 {
  month:"اردیبهشت",
  value:78
 },
 {
  month:"خرداد",
  value:84
 },
 {
  month:"تیر",
  value:88
 },
 {
  month:"مرداد",
  value:92
 }
];


const countyData=[
 {
  name:"زنجان",
  value:95
 },
 {
  name:"ابهر",
  value:89
 },
 {
  name:"خدابنده",
  value:86
 },
 {
  name:"سلطانیه",
  value:93
 },
 {
  name:"طارم",
  value:80
 }
];


const alerts=[
"کاهش پوشش واکسیناسیون تب برفکی در یک شهرستان نیازمند بررسی است.",
"چند پرونده نظارتی بیش از زمان استاندارد در انتظار اقدام هستند.",
"عملکرد آزمایشگاه استان در محدوده مطلوب قرار دارد."
];


const aiItems=[
"روند بیماری‌ها پایش می‌شود.",
"نقاط پرریسک شناسایی می‌شوند.",
"هشدار مدیریتی ایجاد می‌شود."
];


export default function DashboardAdmin(){

const navigate=useNavigate();
const [userDetails, setUserDetails] = useState<UserDetails | null>(null);


useEffect(() => {

    getUserDetails(1)
    .then((data)=>{
        setUserDetails(data);
    })
    .catch((error)=>{
        console.error(
            "User details error:",
            error
        );
    });

}, []);

return (

<div className="dashboard-page" dir="rtl">


<header className="dashboard-header">

<h1>
سامانه مدیریت دامپزشکی
</h1>

<p>
داشبورد هوشمند مدیریتی اداره کل دامپزشکی استان زنجان
</p>
{
userDetails && userDetails.assignments.length > 0 && (

<div className="user-org-info">

<p>
کاربر:
{userDetails.full_name}
</p>

<p>
واحد سازمانی:
{userDetails.assignments[0].organization_unit?.name}
</p>

<p>
سمت:
{userDetails.assignments[0].role?.name}
</p>

</div>

)
}
</header>



<div className="kpi-grid">

{
kpis.map((item,index)=>(

<div
className="kpi-card"
key={index}
onClick={()=>navigate(item.path)}
style={{cursor:"pointer"}}
>

<div className="kpi-icon">
{item.icon}
</div>


<div>

<h4>
{item.title}
</h4>

<strong>
{item.value}
</strong>

<p>
{item.detail}
</p>

</div>


</div>

))
}

</div>





<div className="dashboard-grid">



<section className="panel">

<h3>
عملکرد ادارات
</h3>


<div className="chart-box">

<ResponsiveContainer width="100%" height={300}>

<BarChart data={departmentData}>

<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="name"/>

<YAxis/>

<Tooltip/>

<Bar
dataKey="value"
fill="#2980b9"
/>

</BarChart>

</ResponsiveContainer>


</div>


</section>





<section className="panel">

<h3>
روند واکسیناسیون
</h3>


<div className="chart-box">


<ResponsiveContainer width="100%" height={300}>


<LineChart data={vaccinationTrend}>


<CartesianGrid strokeDasharray="3 3"/>

<XAxis dataKey="month"/>

<YAxis/>

<Tooltip/>


<Line
type="monotone"
dataKey="value"
stroke="#27ae60"
strokeWidth={3}
/>


</LineChart>


</ResponsiveContainer>


</div>


</section>





<section className="panel">


<h3>
عملکرد شهرستان‌ها
</h3>


<div className="chart-box">


<ResponsiveContainer width="100%" height={300}>


<BarChart
data={countyData}
layout="vertical"
>


<XAxis type="number"/>

<YAxis
dataKey="name"
type="category"
/>

<Tooltip/>


<Bar
dataKey="value"
fill="#e67e22"
/>


</BarChart>


</ResponsiveContainer>


</div>


</section>





<section className="panel">


<h3>
وضعیت کلی هشدارها
</h3>


<div className="chart-box">


<ResponsiveContainer width="100%" height={300}>


<PieChart>


<Pie
data={[
{name:"مطلوب",value:70},
{name:"نیازمند اقدام",value:30}
]}
dataKey="value"
outerRadius={100}
>


<Cell fill="#27ae60"/>

<Cell fill="#c0392b"/>


</Pie>


<Tooltip/>


</PieChart>


</ResponsiveContainer>


</div>


</section>



</div>






<section className="panel">


<h3>
هشدارهای مدیریتی
</h3>


{
alerts.map((item,index)=>(

<div
className="status-box"
key={index}
>
⚠️ {item}
</div>

))
}


</section>






<section className="panel">


<h3>
تحلیل هوشمند سیستم
</h3>


{
aiItems.map((item,index)=>(

<p key={index}>
• {item}
</p>

))
}


</section>






<section className="panel">


<h3>
خلاصه عملکرد ادارات
</h3>


<table>


<thead>

<tr>

<th>
اداره
</th>

<th>
شاخص
</th>

<th>
وضعیت
</th>

</tr>

</thead>


<tbody>


{
departmentData.map((item,index)=>(

<tr key={index}>

<td>
{item.name}
</td>

<td>
{item.value}%
</td>

<td>
مطلوب
</td>

</tr>

))
}


</tbody>


</table>


</section>



</div>


)

}
