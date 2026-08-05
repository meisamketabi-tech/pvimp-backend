import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Sidebar.css";

const countyList = [
    { title: "اداره دامپزشکی شهرستان ابهر", path: "/county/ابهر" },
    { title: "اداره دامپزشکی شهرستان ایجرود", path: "/county/ایجرود" },
    { title: "اداره دامپزشکی شهرستان طارم", path: "/county/طارم" },
    { title: "اداره دامپزشکی شهرستان زنجان", path: "/county/زنجان" },
    { title: "اداره دامپزشکی شهرستان خرمدره", path: "/county/خرمدره" },
    { title: "اداره دامپزشکی شهرستان خدابنده", path: "/county/خدابنده" },
    { title: "اداره دامپزشکی شهرستان سلطانیه", path: "/county/سلطانیه" },
    { title: "اداره دامپزشکی شهرستان ماهنشان", path: "/county/ماهنشان" }
];

const menu = [
    {
        title: "حوزه مدیرکل",
        items: [
            ["دفتر مدیرکل", "/"],
            ["نماینده ولی فقیه", "/"],
            ["حراست", "/"],
            ["امور حقوقی", "/"],
            ["روابط عمومی", "/"],
            ["پدافند غیرعامل و مدیریت بحران", "/"]
        ]
    },

    {
        title: "معاونت سلامت",
        items: [
            {
                title: "مدیریت GIS استان",
                submenu: [
                    ["داشبورد GIS استان", "/gis"],

                    {
                        title: "بارگذاری گزارش GIS",
                        submenu: [
                            [
                                "بهداشت و مدیریت بیماری‌های دامی",
                                "/gis/upload/disease-control"
                            ],
                            [
                                "قرنطینه و امنیت زیستی",
                                "/gis/upload/quarantine"
                            ],
                            [
                                "نظارت بهداشت عمومی و مواد غذایی",
                                "/gis/upload/supervision"
                            ],
                            [
                                "طیور و آبزیان",
                                "/gis/upload/poultry"
                            ],
                            [
                                "تشخیص و درمان",
                                "/gis/upload/diagnosis"
                            ],
                            [
                                "آزمایشگاه",
                                "/gis/upload/laboratory"
                            ]
                        ]
                    },

                    ["ورود اطلاعات GIS", "/gis/import"]
                ]
            },

            [
                "اداره بهداشت و مدیریت بیماری‌های دامی",
                "/disease-control"
            ],

            {
                title: "اداره نظارت بر بهداشت عمومی و مواد غذایی",
                submenu: [
                    ["داشبورد نظارت", "/supervision"],
                    ["ثبت فرم بازرسی جدید", "/supervision/create"],
                    ["لیست بازرسی‌ها", "/supervision/list"],
                    ["گزارشات", "/supervision/reports"],
                    ["GIS", "/gis/departments"],
                    ["تخلفات", "/supervision/violations"],
                    ["نمونه‌برداری", "/supervision/samples"],
                    ["امور حقوقی", "/supervision/legal"],
                    ["تنظیمات", "/supervision/settings"]
                ]
            },

            ["قرنطینه و امنیت زیستی", "/quarantine"],

            [
                "اداره بهداشت طیور، زنبورعسل، کرم ابریشم و آبزیان",
                "/poultry"
            ],

            {
                title: "اداره تشخیص و درمان",
                submenu: [
                    ["آزمایشگاه", "/laboratory"]
                ]
            }
        ]
    },

    {
        title: "معاونت توسعه و مدیریت منابع",
        items: [
            ["امور پشتیبانی و رفاه", "/"],
            ["امور مالی", "/"],
            ["فناوری اطلاعات و تحول اداری", "/"],
            ["طرح، برنامه و بودجه", "/"]
        ]
    }
];

interface SidebarProps {
    mobileOpen?: boolean;
    onMobileClose?: () => void;
}

export default function Sidebar({
    mobileOpen = false,
    onMobileClose
}: SidebarProps) {

    const navigate = useNavigate();

    const [openMain, setOpenMain] = useState<number | null>(null);
    const [openSub, setOpenSub] = useState<string[]>([]);
    const [openCounty, setOpenCounty] = useState<string | null>(null);

    function handleNavigate(path: string) {
        navigate(path);

        if (window.innerWidth <= 900 && onMobileClose) {
            onMobileClose();
        }
    }

    function renderSubmenu(items: any[]) {

        return items.map((item: any, index: number) => {

            if (Array.isArray(item)) {

                return (
                    <div
                        key={index}
                        className="tree-child"
                        onClick={() => handleNavigate(item[1])}
                    >
                        {item[0]}
                    </div>
                );
            }

            return (
                <div key={index}>

                    <div
                        className="tree-title"
                        onClick={() => {

                            setOpenSub(prev =>
                                prev.includes(item.title)
                                    ? prev.filter(x => x !== item.title)
                                    : [...prev, item.title]
                            );

                        }}
                    >

                        <span>
                            {openSub.includes(item.title) ? "−" : "+"}
                        </span>

                        {item.title}

                    </div>

                    {openSub.includes(item.title) && item.submenu && (
                        <div className="tree-children">
                            {renderSubmenu(item.submenu)}
                        </div>
                    )}

                </div>
            );
        });
    }

    return (

        <aside
            className={`sidebar ${mobileOpen ? "sidebar-mobile-open" : ""}`}
            dir="rtl"
        >

            <div className="sidebar-header">

                <button
                    className="sidebar-mobile-close"
                    onClick={onMobileClose}
                    aria-label="بستن منو"
                >
                    ×
                </button>

                <h2>
                    سامانه مدیریت یکپارچه دامپزشکی
                </h2>

                <p>
                    استان زنجان
                </p>

            </div>

            <div className="tree-menu">

                {menu.map((group, index) => (

                    <div key={index}>

                        <div
                            className="tree-title"
                            onClick={() =>
                                setOpenMain(
                                    openMain === index
                                        ? null
                                        : index
                                )
                            }
                        >

                            <span>
                                {openMain === index ? "−" : "+"}
                            </span>

                            {group.title}

                        </div>

                        {openMain === index && (
                            <div className="tree-children">
                                {renderSubmenu(group.items)}
                            </div>
                        )}

                    </div>

                ))}

                <div
                    className="tree-title"
                    onClick={() =>
                        setOpenMain(
                            openMain === 99
                                ? null
                                : 99
                        )
                    }
                >

                    <span>
                        {openMain === 99 ? "−" : "+"}
                    </span>

                    ادارات شهرستان

                </div>

                {openMain === 99 && (

                    <div className="tree-children">

                        {countyList.map((county, index) => (

                            <div key={index}>

                                <div
                                    className="tree-title county-menu"
                                    onClick={() =>
                                        setOpenCounty(
                                            openCounty === county.path
                                                ? null
                                                : county.path
                                        )
                                    }
                                >

                                    <span>
                                        {openCounty === county.path
                                            ? "−"
                                            : "+"}
                                    </span>

                                    {county.title}

                                </div>

                                {openCounty === county.path && (

                                    <div className="tree-children">

                                        <div
                                            className="tree-child"
                                            onClick={() =>
                                                handleNavigate(county.path)
                                            }
                                        >
                                            داشبورد مدیریتی شهرستان
                                        </div>

                                        <div
                                            className="tree-child"
                                            onClick={() =>
                                                handleNavigate(
                                                    county.path +
                                                    "/expert/supervision"
                                                )
                                            }
                                        >
                                            کارشناس نظارت و بازرسی
                                        </div>

                                        <div
                                            className="tree-child"
                                            onClick={() =>
                                                handleNavigate(
                                                    county.path +
                                                    "/expert/disease"
                                                )
                                            }
                                        >
                                            کارشناس مدیریت بیماری‌ها
                                        </div>

                                    </div>

                                )}

                            </div>

                        ))}

                    </div>

                )}

            </div>

        </aside>
    );
}