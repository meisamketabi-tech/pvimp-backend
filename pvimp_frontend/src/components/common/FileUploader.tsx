
import React,{useState} from "react";


import {
uploadAttachment
}
from "../../services/attachmentService";



export default function FileUploader(
{
entity,
entityId
}:any
){


const [file,setFile]=useState<File|null>(null);



const upload=()=>{

if(file)

uploadAttachment(
entity,
entityId,
file
);

};



return (

<div dir="rtl">


<input

type="file"

onChange={
e=>
setFile(
e.target.files?.[0] || null
)
}

/>


<button
onClick={upload}
>
بارگذاری فایل
</button>


</div>

)

}
