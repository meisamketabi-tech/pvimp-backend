
import axios from "axios";


const API="http://localhost:8000/workflow";



export const createTask=(data:any)=>
axios.post(
`${API}/create`,
data
);



export const updateTaskStatus=(
id:number,
status:string
)=>
axios.put(
`${API}/${id}/status?status=${status}`
);



export const getTasks=()=>
axios.get(
`${API}/`
);

