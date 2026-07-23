const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://localhost:8000/api/v1";


export async function getSupervisionInspections(){

    const response = await fetch(
        `${API_URL}/inspections`
    );


    if(!response.ok){
        throw new Error(
            "خطا در دریافت اطلاعات بازرسی"
        );
    }


    return await response.json();

}



export async function createSupervisionInspection(
    data:any
){

    const payload = {

        inspection_type_id:3,

        organization_unit_id:18,

        veterinary_unit_id:1,

        inspector_id:7,

        inspection_date:
            data.inspectionDate ||
            new Date().toISOString(),

        notes:
            `
نوع بازرسی: ${data.inspectionType || ""}
نام واحد: ${data.unitName || ""}
نوع واحد: ${data.unitType || ""}
نام مالک: ${data.ownerName || ""}
تلفن: ${data.phone || ""}
شهرستان: ${data.city || ""}
آدرس: ${data.address || ""}
بازرس: ${data.inspectorName || ""}
`
    };


    const response = await fetch(

        `${API_URL}/inspections`,

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(payload)

        }

    );


    if(!response.ok){

        throw new Error(
            "خطا در ثبت بازرسی"
        );

    }


    return await response.json();

}