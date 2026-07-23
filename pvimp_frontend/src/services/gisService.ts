export interface GISCenter {


id:number;

name:string;

type:string;

lat:number;

lng:number;

risk:string;

lastVisit:string;


}



export async function getGISCenters(countyId:string){


const data:GISCenter[]=[


{

id:1,

name:"فروشگاه مواد خام دامی الف",

type:"عرضه فرآورده خام دامی",

lat:36.55,

lng:48.25,

risk:"high",

lastVisit:"1405/04/10"

},



{

id:2,

name:"کشتارگاه شهرستان",

type:"کشتارگاه",

lat:36.56,

lng:48.26,

risk:"medium",

lastVisit:"1405/04/15"

}



];


return data;


}