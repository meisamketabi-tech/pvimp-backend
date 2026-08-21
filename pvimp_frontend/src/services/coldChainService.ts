
import axios from "axios";


const API="http://localhost:8000/cold-chain";



export const getColdChainLogs=()=>
axios.get(API);



export const getColdChainAlerts=()=>
axios.get(
`${API}/alerts`
);

