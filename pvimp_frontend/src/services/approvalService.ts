
import axios from "axios";


const API="http://localhost:8000/approval";



export const getApprovalRequests=()=>
axios.get(API);



export const reviewApproval=(
id:number,
status:string,
comment:string=""
)=>
axios.put(
`${API}/${id}?status=${status}&comment=${comment}`
);

