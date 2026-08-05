export interface SupervisionInspection {

    sampleType: string;


    inspectionId?: number;
    inspectionNumber?: string;
    inspectionDate: string;
    inspectionType: string;
    inspectionStatus?: string;

    partners: string[];

    centerType: string;
    unitType: string;
    slaughterType: string[];
    selectedSlaughter: string;

    unitName: string;
    ownerName: string;
    phone: string;

    province: string;
    city: string;
    address: string;

    inspectorName: string;

    nonComplianceCount: number;
    judicialReferral: boolean;
    sampling: boolean;


sampleCount: number;

    destroyedProductKg: number;

    violations: string[];
    sealed: boolean;

    description: string;
}

export const emptyInspection: SupervisionInspection = {

    sampleType: "",


    inspectionDate: "",
    inspectionType: "",
    partners: [],
    centerType: "",
    unitType: "",
    slaughterType: [],
    selectedSlaughter: "",
    unitName: "",
    ownerName: "",
    phone: "",
    province: "?????",
    city: "",
    address: "",
    inspectorName: "",
    inspectionStatus: "draft",
    nonComplianceCount: 0,
    judicialReferral: false,
    sampling: false,
    sampleCount: 0,
    destroyedProductKg: 0,
    violations: [],
    sealed: false,
    description: ""
};
