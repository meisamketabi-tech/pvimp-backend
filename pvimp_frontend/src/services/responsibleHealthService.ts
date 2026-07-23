
import axios from "axios";


const API="http://localhost:8000/responsible-health";



export const getStatistics=()=> 
axios.get(`${API}/statistics`);



export const getComplianceScore=(id:number)=>
axios.get(`${API}/compliance-score/${id}`);



export const getOfficerSummary=(id:number)=>
axios.get(`${API}/officer/${id}/summary`);
