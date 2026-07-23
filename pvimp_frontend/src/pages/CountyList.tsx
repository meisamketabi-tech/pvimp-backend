import React from "react";
import {useNavigate} from "react-router-dom";
import "./Dashboard.css";


const counties=[

"اداره دامپزشکی شهرستان ابهر",
"اداره دامپزشکی شهرستان ایجرود",
"اداره دامپزشکی شهرستان طارم",
"اداره دامپزشکی شهرستان زنجان",
"اداره دامپزشکی شهرستان خرمدره",
"اداره دامپزشکی شهرستان خدابنده",
"اداره دامپزشکی شهرستان سلطانیه",
"اداره دامپزشکی شهرستان ماهنشان"

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

onClick={()=>navigate(`/county/${index}`)}

style={{
cursor:"pointer"
}}

>

<h3>
{county}
</h3>

<p>
مشاهده رئیس اداره و کارشناسان
</p>


</div>

))

}


</div>


</div>

)

}
