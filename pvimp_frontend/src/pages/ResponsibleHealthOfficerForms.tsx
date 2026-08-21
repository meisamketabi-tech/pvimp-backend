
import React,{useState} from "react";
import {
createOfficer,
createInspection,
createNonConformity,
createSample,
createColdChain
}
from "../services/responsibleHealthService";

import "./Dashboard.css";


export default function ResponsibleHealthOfficerForms(){


const [form,setForm]=useState("officer");


const [data,setData]=useState<any>({});


const change=(e:any)=>
setData({...data,[e.target.name]:e.target.value});



const submit=async()=>{


if(form==="officer")
await createOfficer(data);


if(form==="inspection")
await createInspection(data);


if(form==="non")
await createNonConformity(data);


if(form==="sample")
await createSample(data);


if(form==="cold")
await createColdChain(data);


alert("ثبت شد");


setData({});

};



return (

<div className="dashboard-container" dir="rtl">


<h1>
فرم‌های مسئول بهداشتی
</h1>



<div className="form-menu">

<button onClick={()=>setForm("officer")}>
پرونده مسئول
</button>

<button onClick={()=>setForm("inspection")}>
بازدید
</button>

<button onClick={()=>setForm("non")}>
عدم انطباق
</button>

<button onClick={()=>setForm("sample")}>
نمونه برداری
</button>

<button onClick={()=>setForm("cold")}>
زنجیره سرد
</button>


</div>




<div className="dashboard-card">


{form==="officer" &&

<>
<h2>پرونده مسئول بهداشتی</h2>

<input name="full_name" placeholder="نام" onChange={change}/>

<input name="national_code" placeholder="کد ملی" onChange={change}/>

<input name="license_number" placeholder="شماره پروانه" onChange={change}/>

<input name="unit_name" placeholder="نام واحد" onChange={change}/>

</>

}



{form==="inspection" &&

<>
<h2>بازدید</h2>

<input name="inspection_date" type="date" onChange={change}/>

<input name="employee_status" placeholder="وضعیت کارکنان" onChange={change}/>

<input name="building_status" placeholder="وضعیت ساختمان" onChange={change}/>

<textarea name="description" onChange={change}/>

</>

}



{form==="non" &&

<>
<h2>عدم انطباق</h2>

<input name="title" placeholder="عنوان تخلف" onChange={change}/>

<input name="level" placeholder="سطح تخلف" onChange={change}/>

<textarea name="description" onChange={change}/>

</>

}



{form==="sample" &&

<>
<h2>نمونه برداری</h2>

<input name="sample_type" placeholder="نوع نمونه" onChange={change}/>

<input name="product_name" placeholder="محصول" onChange={change}/>

<input name="batch_number" placeholder="شماره بچ" onChange={change}/>

</>

}



{form==="cold" &&

<>
<h2>زنجیره سرد</h2>

<input name="location" placeholder="محل" onChange={change}/>

<input name="temperature" placeholder="دما" onChange={change}/>

<input name="status" placeholder="وضعیت" onChange={change}/>

</>

}




<button onClick={submit}>
ثبت اطلاعات
</button>


</div>


</div>


)

}

