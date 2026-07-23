export interface SupervisionInspectionForm {

  inspectionDate:string;
  inspectionType:string;

  county:string;
  epidemiologyUnitId:string;
  epidemiologyUnitCode:string;

  unitName:string;
  unitType:string;

  ownerName:string;
  nationalId:string;
  phone:string;

  province:string;
  city:string;
  village:string;
  address:string;

  latitude:string;
  longitude:string;

  gpsVerified:boolean;

  inspectorName:string;

  inspectionResult:string;

  violations:string[];

  samplesTaken:number;

  sampleDescription:string;

  judicialReferral:boolean;

  sealed:boolean;

  destroyedProductsKg:number;

  confiscatedProductsKg:number;

  notes:string;

}

export interface GISSlaughterRecord{

  sanitaryInspectionVCode:string;

  certificateNumber:string;

  certificateDate:string;

  registerDate:string;

  epidemiologyUnitName:string;

  epidemiologyUnitCode:string;

  epidemiologyUnitType:string;

  province:string;

  county:string;

  sourceUnitName:string;

  sourceUnitType:string;

  operationType:string;

  diseaseName:string;

  animalType:string;

  seizureType:string;

  organ:string;

  count:number;

  weight:number;

}
