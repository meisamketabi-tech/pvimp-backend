import React from "react";

export default function KpiCard({
    title,
    value,
    icon,
    status,
    onClick
}: any) {

    return (

        <div
            className={"manager-kpi " + (status || "")}
            onClick={onClick}
        >


            <div className="manager-kpi-icon">
                {icon}
            </div>


            <div>


                <div className="manager-kpi-title">
                    {title}
                </div>


                <div className="manager-kpi-value">
                    {value}
                </div>


                <div className="manager-kpi-link">
                    مشاهده جزئیات
                </div>


            </div>


        </div>

    );

}