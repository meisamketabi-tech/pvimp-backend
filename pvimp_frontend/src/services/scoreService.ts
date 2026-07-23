
import axios from "axios";


const API="http://localhost:8000/scores";



export const getScores=()=>
axios.get(API);



export const getUnitScore=(id:number)=>
axios.get(
`${API}/${id}`
);

