import React from "react";

export default function DepartmentCard() {

    const data = [

        ["واحد دامپزشکی", "95%"],

        ["کنترل بیماری", "87%"],

        ["واکسیناسیون", "92%"],

        ["آزمایشگاه", "94%"],

        ["GIS", "89%"]

    ];


    return (

        <div className="dashboard-box">


            <h2>
                عملکرد واحدها
            </h2>



            {
                data.map((d, i) => (

                    <div
                        className="department-row"
                        key={i}
                    >

                        <span>
                            {d[0]}
                        </span>


                        <strong>
                            {d[1]}
                        </strong>


                    </div>

                ))
            }



        </div>

    );

}