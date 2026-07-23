export interface SupervisionInspection {

inspectionDate:string;

inspectionType:string;

partners:string[];

centerType:string;

unitType:string;

slaughterType:string[];

selectedSlaughter:string;

unitName:string;

ownerName:string;

phone:string;

province:string;

city:string;

address:string;

inspectorName:string;

}



export const emptyInspection:SupervisionInspection={

inspectionDate:"",

inspectionType:"",

partners:[],

centerType:"",

unitType:"",

slaughterType:[],

selectedSlaughter:"",

unitName:"",

ownerName:"",

phone:"",

province:"زنجان",

city:"",

address:"",

inspectorName:""

};