
import axios from "axios";


const API="http://localhost:8000/audit";



export const getAuditLogs=()=>
axios.get(API);

