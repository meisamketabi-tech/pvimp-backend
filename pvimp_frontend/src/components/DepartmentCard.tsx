import React from "react";

type DepartmentItem = {
    title: string;
    value: string;
};

type DepartmentCardProps = {
    title?: string;
    data?: DepartmentItem[];
};

const defaultData: DepartmentItem[] = [
    { title: "بهداشت عمومی", value: "95%" },
    { title: "بیماری‌های دامی", value: "87%" },
    { title: "قرنطینه", value: "92%" },
    { title: "تشخیص و درمان", value: "94%" },
    { title: "نظارت", value: "89%" }
];

export default function DepartmentCard({
    title = "وضعیت عملکرد ادارات",
    data = defaultData
}: DepartmentCardProps) {
    return (
        <section
            className="pv-department-card"
            dir="rtl"
        >
            <h3>{title}</h3>

            <div className="pv-department-list">
                {data.map((item, index) => (
                    <div
                        className="pv-department-row"
                        key={`${item.title}-${index}`}
                    >
                        <span>{item.title}</span>
                        <strong>{item.value}</strong>
                    </div>
                ))}
            </div>
        </section>
    );
}