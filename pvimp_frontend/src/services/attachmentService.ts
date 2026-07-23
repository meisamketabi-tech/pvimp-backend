
import axios from "axios";


const API="http://localhost:8000/attachments";



export const uploadAttachment=(

entity:string,

id:number,

file:File,

description:string=""

)=>{


const form=new FormData();


form.append(
"entity_type",
entity
);


form.append(
"entity_id",
id.toString()
);


form.append(
"description",
description
);


form.append(
"file",
file
);



return axios.post(
API,
form,
{
headers:{
"Content-Type":"multipart/form-data"
}
}
);


};



export const getAttachments=(

entity:string,

id:number

)=>

axios.get(
`${API}/${entity}/${id}`
);

