
import axios from "axios";


const API="http://localhost:8000/checklists";



export const getChecklists=()=>
axios.get(API);



export const getChecklistItems=(id:number)=>
axios.get(
`${API}/${id}/items`
);

