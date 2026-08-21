import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";


const forms = [

{
title:"واحدهای اپیدمیولوژیک",
file:"واحدهاي اپيدميولوژيک.xls"
},

{
title:"واحدهای فعال (گزارش 117)",
file:"واحد هاي فعال(گزارش 117).xls"
},

{
title:"گزارش بیماری",
file:"گزارش بيماري.xlsx"
},

{
title:"گزارش بروز بیماری دام",
file:"گزارش بروز بيماري دام.xlsx"
},

{
title:"گزارش سابقه عملیات در واحد دامی (107)",
file:"گزارش سابقه عمليات در واحد دامي - 107.xlsx"
},

{
title:"گزارش عملکرد پایش مراقبت (106)",
file:"گزارش عملکرد پايش مراقبت - 106.xlsx"
},

{
title:"گزارش پایش مراقبت واحدهای دامی (105)",
file:"گزارش پايش مراقبت واحدهاي دامي - 105.xlsx"
},

{
title:"گزارش واکسیناسیون واحدهای دامی",
file:"گزارش واکسيناسيون واحدهاي دامي.xlsx"
},

{
title:"توزیع واکسن",
file:"توزيع واکسن.xlsx"
}

];



export default function ExcelImport(){


const navigate = useNavigate();


const [files,setFiles]=useState<{[key:string]:File|null}>({});



const handleFile=(name:string,file:File|null)=>{

setFiles({

...files,

[name]:file

});

};



const uploadedCount = Object.values(files)
.filter(item=>item !== null)
.length;



return(


<div className="dashboard-container" dir="rtl">



<div className="expert-header">


<h1>
مرکز بارگذاری اطلاعات GIS
</h1>


<p>
دریافت و ثبت فایل‌های پایه سامانه GIS برای تحلیل مراقبت و مدیریت بیماری‌ها
</p>


</div>






<div className="cards">


<div className="card">

<h3>
تعداد فرم‌ها
</h3>

<strong>
{forms.length}
</strong>

<p>
فرم مورد نیاز GIS
</p>

</div>




<div className="card">

<h3>
فایل‌های انتخاب شده
</h3>

<strong>
{uploadedCount}
</strong>

<p>
آماده ارسال
</p>

</div>




<div className="card county-card">

<h3>
وضعیت بارگذاری
</h3>

<strong>
{uploadedCount === forms.length ? "کامل" : "ناقص"}
</strong>

<p>
وضعیت دریافت داده
</p>

</div>


</div>







<div className="panel">


<h2>
فایل‌های مورد نیاز GIS
</h2>




<div className="excel-import-list">


{

forms.map((form,index)=>(


<div className="excel-upload-card" key={index}>


<div className="excel-card-header">


<h3>
{form.title}
</h3>


<span>

{

files[form.file]

?

"انتخاب شده"

:

"دریافت نشده"

}

</span>


</div>





<label className="file-label">


📂 انتخاب فایل



<input

type="file"

accept=".xls,.xlsx"

onChange={(e)=>

handleFile(

form.file,

e.target.files?.[0] || null

)

}

/>


</label>





<div className="selected-file">


{

files[form.file]

?

files[form.file]?.name

:

"فایلی انتخاب نشده"

}


</div>





<button className="upload-btn">

ارسال فایل

</button>





</div>


))


}


</div>


</div>







<div className="panel back-panel">


<button

className="back-btn"

onClick={()=>navigate(-1)}

>

⬅ بازگشت به داشبورد

</button>


</div>




</div>


)

}

