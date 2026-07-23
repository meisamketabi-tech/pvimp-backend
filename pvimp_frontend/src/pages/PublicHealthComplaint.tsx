
import React,{useState} from "react";


import {
submitComplaint
}
from "../services/complaintPublicService";


import "./Dashboard.css";



export default function PublicHealthComplaint(){


const [form,setForm]=useState<any>({});

const [message,setMessage]=useState("");



const submit=()=>{


submitComplaint(form)
.then(()=>{

setMessage(
"شکایت با موفقیت ثبت شد"
);

setForm({});

});


};



return (

<div className="dashboard-container" dir="rtl">


<h1>
ثبت شکایت بهداشتی
</h1>



<div className="dashboard-card">


<input

placeholder="نام"

value={form.complainant_name || ""}

onChange={
e=>
setForm({
...form,
complainant_name:e.target.value
})
}

/>



<input

placeholder="شماره تماس"

value={form.contact || ""}

onChange={
e=>
setForm({
...form,
contact:e.target.value
})
}

/>



<input

placeholder="موضوع"

value={form.subject || ""}

onChange={
e=>
setForm({
...form,
subject:e.target.value
})
}

/>



<textarea

placeholder="شرح شکایت"

value={form.description || ""}

onChange={
e=>
setForm({
...form,
description:e.target.value
})
}

/>



<button
onClick={submit}
>
ثبت شکایت
</button>



<h3>
{message}
</h3>


</div>


</div>

)

}
