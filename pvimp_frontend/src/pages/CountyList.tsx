import React from "react";
import {useNavigate} from "react-router-dom";
import "./Dashboard.css";


const counties=[

{title:"اداره دامپزشکی شهرستان ابهر",id:"ابهر"},
{title:"اداره دامپزشکی شهرستان ایجرود",id:"ایجرود"},
{title:"اداره دامپزشکی شهرستان طارم",id:"طارم"},
{title:"اداره دامپزشکی شهرستان زنجان",id:"زنجان"},
{title:"اداره دامپزشکی شهرستان خرمدره",id:"خرمدره"},
{title:"اداره دامپزشکی شهرستان خدابنده",id:"خدابنده"},
{title:"اداره دامپزشکی شهرستان سلطانیه",id:"سلطانیه"},
{title:"اداره دامپزشکی شهرستان ماهنشان",id:"ماهنشان"}

];



export default function CountyList(){

const navigate=useNavigate();


return(

<div className="dashboard-page" dir="rtl">


<div className="dashboard-header">

<h1>
ادارات دامپزشکی شهرستان استان زنجان
</h1>

<p>
انتخاب اداره شهرستان جهت ورود به ساختار مدیریتی
</p>

</div>



<div className="dashboard-grid">


{

counties.map((county,index)=>(

<div

className="dashboard-box"

key={index}

onClick={()=>navigate(`/county/${encodeURIComponent(county.id)}`)}

style={{
cursor:"pointer"
}}

>

<h3>
{county.title}
</h3>

<p>
مشاهده داشبورد مدیریتی شهرستان
</p>


</div>

))

}


</div>


</div>

)

}