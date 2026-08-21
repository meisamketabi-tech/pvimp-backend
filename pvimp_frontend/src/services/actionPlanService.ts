
import axios from "axios";


const API="http://localhost:8000/actions";



export const getActions=()=>
axios.get(API);



export const completeAction=(id:number)=>
axios.put(
`${API}/${id}/complete`
);

