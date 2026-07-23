import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";


const forms = [

{
title:"گزارش بازدید مراکز عرضه فرآورده خام دامی",
file:"raw_products_inspection.xlsx"
},

{
title:"گزارش بازدید رستوران‌ها و مراکز طبخ",
file:"restaurants_inspection.xlsx"
},

{
title:"گزارش بازدید کشتارگاه‌ها",
file:"slaughterhouse_inspection.xlsx"
},

{
title:"گزارش بازدید سردخانه‌ها",
file:"cold_storage_inspection.xlsx"
},

{
title:"گزارش تخلفات بهداشتی",
file:"health_violations.xlsx"
},

{
title:"گزارش اقدامات اصلاحی",
file:"corrective_actions.xlsx"
},

{
title:"گزارش نمونه‌برداری و نتایج آزمایشگاهی",
file:"sampling_results.xlsx"
},

{
title:"گزارش شکایات مردمی",
file:"public_complaints.xlsx"
}

];



export default function SupervisionImport(){


const navigate = useNavigate();


const [files,setFiles]=useState<{[key:string]:File|null}>({});



const handleFile=(name:string,file:File|null)=>{


setFiles({

...files,

[name]:file

});


};



const uploadedCount = Object.values(files)
.filter(item=>item!==null)
.length;



return(


<div className="dashboard-container" dir="rtl">



<div className="expert-header">


<h1>
مرکز ورود اطلاعات اداره نظارت
</h1>


<p>
بارگذاری گزارش‌های بازدید، تخلفات و نتایج پایش بهداشتی
</p>


</div>






<div className="cards">


<div className="card county-card">

<h3>
تعداد فرم‌ها
</h3>

<strong>
{forms.length}
</strong>

<p>
فرم نظارتی
</p>

</div>



<div className="card">

<h3>
فایل انتخاب شده
</h3>

<strong>
{uploadedCount}
</strong>

<p>
آماده ارسال
</p>

</div>



<div className="card">

<h3>
وضعیت دریافت
</h3>

<strong>
{

uploadedCount === forms.length

?

"کامل"

:

"ناقص"

}

</strong>

<p>
اطلاعات نظارت
</p>

</div>


</div>







<div className="panel">


<h2>
فرم‌های مورد نیاز اداره نظارت
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


📂 انتخاب فایل Excel



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

⬅ بازگشت به داشبورد نظارت

</button>



</div>




</div>


)

}