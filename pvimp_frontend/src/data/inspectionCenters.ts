export interface SupervisionInspection {


id?:number;


inspectionDate:string;


inspectionType:string;


city:string;



centerType:string;


slaughterType:string;


slaughterhouse:string;



unitType:string;


unitName:string;


ownerName:string;


phone:string;


address:string;


inspectorName:string;



partners:string[];


}



export const emptyInspection:SupervisionInspection={


inspectionDate:"",


inspectionType:"",


city:"",



centerType:"",


slaughterType:"",


slaughterhouse:"",



unitType:"",


unitName:"",


ownerName:"",


phone:"",


address:"",


inspectorName:"",



partners:[]

};