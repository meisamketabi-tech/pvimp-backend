
import axios from "axios";


const API="http://localhost:8000/alerts";



export const getHealthAlerts=()=>
axios.get(API);



export const updateHealthAlert=(
id:number,
status:string
)=>
axios.put(
`${API}/${id}?status=${status}`
);

