
import axios from "axios";


const API="http://localhost:8000/permits";



export const getPermits=()=>
axios.get(API);



export const getUnitPermits=(id:number)=>
axios.get(
`${API}/unit/${id}`
);

