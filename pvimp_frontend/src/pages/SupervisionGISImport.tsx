import React, {useState} from "react";
import {useParams, useNavigate} from "react-router-dom";
import "./SupervisionGISImport.css";

export default function SupervisionGISImport(){

const {id}=useParams();
const navigate=useNavigate();

const [file,setFile]=useState<File|null>(null);
const [status,setStatus]=useState("دریافت نشده");


const uploadFile=()=>{

if(!file){
alert("ابتدا فایل را انتخاب کنید");
return;
}

setStatus("فایل دریافت شد");

};


return(

<div
className="dashboard-container"
dir="rtl"
>


<div className="expert-header">

<h1>
مرکز بارگذاری اطلاعات GIS نظارت بهداشتی
</h1>

<p>
شهرستان {id}
</p>

</div>



<div className="dashboard-box">


<h2>
دریافت فایل خروجی سامانه GIS
</h2>


<p>
فایل Excel گزارش‌های نظارت بهداشتی جهت تحلیل بازرسی‌ها و مدیریت ریسک واحدها
</p>



<div className="form-section">


<h3>
فایل اطلاعات نظارت بهداشتی
</h3>


<div>

<input

type="file"

accept=".xlsx,.xls"

onChange={(e)=>{

setFile(
e.target.files?.[0] || null
)

}}

/>


</div>



<p>

وضعیت دریافت:

<strong>

{" "}{status}

</strong>

</p>



<button

className="upload-btn"

onClick={uploadFile}

>

ارسال فایل

</button>


</div>



<div className="form-section">


<h3>
اطلاعات فایل
</h3>


<ul>

<li>
SanitaryInspectionVCode
</li>

<li>
شماره گواهی
</li>

<li>
تاریخ گواهی
</li>

<li>
نام واحد اپیدمیولوژیک
</li>

<li>
کد واحد اپیدمیولوژیک
</li>

<li>
نوع واحد اپیدمیولوژیک
</li>

<li>
نوع عملیات
</li>

<li>
نوع دام
</li>

<li>
نوع ضبط
</li>

<li>
اندام
</li>

<li>
تعداد و وزن
</li>

<li>
EpidemiologyUnitId
</li>


</ul>


</div>



<button

className="upload-btn"

onClick={()=>navigate(
`/county/${id}/expert/supervision`
)}

>

⬅ بازگشت به داشبورد

</button>



</div>


</div>

)

}