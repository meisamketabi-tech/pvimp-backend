
import axios from "axios";


const API="http://localhost:8000/risk";



export const getRisks=()=>
axios.get(API);



export const getHighRisks=()=>
axios.get(
`${API}/high`
);



export const createRisk=(data:any)=>
axios.post(
API,
data
);
