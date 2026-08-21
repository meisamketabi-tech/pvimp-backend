
import axios from "axios";


const API="http://localhost:8000/violations";



export const getViolations=()=>
axios.get(API);



export const getUnitViolations=(id:number)=>
axios.get(
`${API}/unit/${id}`
);

