import React, {useState} from "react";


export default function GISUploader(){

const [file,setFile]=useState<File|null>(null);


function handleUpload(){

if(!file){
alert("ابتدا فایل GIS را انتخاب کنید");
return;
}

alert(
"فایل آماده ارسال به سامانه است: "+file.name
);

}


return(

<div className="dashboard-box" dir="rtl">

<h2>
دریافت اطلاعات GIS
</h2>


<p>
بارگذاری خروجی Excel سامانه GIS
</p>


<input
type="file"
accept=".xlsx,.xls"
onChange={(e)=>
setFile(e.target.files?.[0] || null)
}
/>


<button
onClick={handleUpload}
style={{
marginRight:"10px",
padding:"8px 20px"
}}
>

بارگذاری

</button>


{
file &&
<p>
فایل انتخاب شده:
{file.name}
</p>
}


</div>

)

}
