
import React, {useEffect, useState} from "react";
import {
    getInspections,
    Inspection
} from "../services/inspectionService";


export default function InspectionDashboard(){

    const [data,setData] = useState<Inspection[]>([]);

    useEffect(()=>{

        getInspections()
            .then(response => setData(response.data))
            .catch(err=>console.error(err));

    },[]);


    return (

        <div dir="rtl">

            <h1>
                ??????? ?????? ??
            </h1>


            <table border={1} width="100%">

                <thead>

                <tr>
                    <th>?????</th>
                    <th>?????</th>
                    <th>?????</th>
                    <th>?????</th>
                </tr>

                </thead>


                <tbody>

                {
                    data.map(item=>(

                        <tr key={item.id}>

                            <td>
                                {item.inspection_number}
                            </td>

                            <td>
                                {item.inspection_date}
                            </td>

                            <td>
                                {item.status}
                            </td>

                            <td>
                                {item.result}
                            </td>

                        </tr>

                    ))
                }

                </tbody>

            </table>


        </div>

    )

}
