
import axios from "axios";


const API="http://localhost:8000/complaints";



export const getComplaints=()=>
axios.get(API);



export const updateComplaint=(
id:number,
status:string
)=>
axios.put(
`${API}/${id}?status=${status}`
);
