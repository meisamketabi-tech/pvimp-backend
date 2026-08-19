import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Sidebar.css";

type MenuLeaf = [title: string, path: string];
type MenuBranch = { title: string; submenu: MenuItem[] };
type MenuItem = MenuLeaf | MenuBranch;
type MenuGroup = { title: string; items: MenuItem[] };
type CountyItem = { title: string; path: string };

const countyList: CountyItem[] = [
    { title: "اداره دامپزشکی شهرستان ابهر", path: "/county/ابهر" },
    { title: "اداره دامپزشکی شهرستان ایجرود", path: "/county/ایجرود" },
    { title: "اداره دامپزشکی شهرستان طارم", path: "/county/طارم" },
    { title: "اداره دامپزشکی شهرستان زنجان", path: "/county/زنجان" },
    { title: "اداره دامپزشکی شهرستان خرمدره", path: "/county/خرمدره" },
    { title: "اداره دامپزشکی شهرستان خدابنده", path: "/county/خدابنده" },
    { title: "اداره دامپزشکی شهرستان سلطانیه", path: "/county/سلطانیه" },
    { title: "اداره دامپزشکی شهرستان ماهنشان", path: "/county/ماهنشان" }
];

const menu: MenuGroup[] = [
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

            [
                "قرنطینه و امنیت زیستی",
                "/quarantine"
            ],

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

    function toggleSubmenu(title: string) {
        setOpenSub((prev) =>
            prev.includes(title)
                ? prev.filter((item) => item !== title)
                : [...prev, title]
        );
    }

    function renderSubmenu(items: MenuItem[]) {
        return items.map((item, index) => {

            if (Array.isArray(item)) {
                return (
                    <button
                        key={index}
                        type="button"
                        className="tree-child"
                        onClick={() => handleNavigate(item[1])}
                    >
                        <span className="tree-child-text">
                            {item[0]}
                        </span>
                    </button>
                );
            }

            const isOpen = openSub.includes(item.title);

            return (
                <div key={index} className="tree-node">

                    <button
                        type="button"
                        className="tree-title tree-title-nested"
                        onClick={() => toggleSubmenu(item.title)}
                        aria-expanded={isOpen}
                    >
                        <span
                            className="tree-toggle"
                            aria-hidden="true"
                        >
                            {isOpen ? "−" : "+"}
                        </span>

                        <span className="tree-text">
                            {item.title}
                        </span>
                    </button>

                    {isOpen && item.submenu && (
                        <div className="tree-children">
                            {renderSubmenu(item.submenu)}
                        </div>
                    )}

                </div>
            );
        });
    }

    return (
        <>
            {mobileOpen && (
                <div
                    className="sidebar-mobile-backdrop"
                    onClick={onMobileClose}
                    aria-hidden="true"
                />
            )}

            <aside
                className={`sidebar ${
                    mobileOpen ? "sidebar-mobile-open" : ""
                }`}
                dir="rtl"
            >
                <div className="sidebar-header">

                    <div className="sidebar-brand">
                        <div className="sidebar-logo">
                            دام
                        </div>

                        <div className="sidebar-title">
                            <strong>
                                سامانه مدیریت یکپارچه دامپزشکی
                            </strong>

                            <span>
                                استان زنجان
                            </span>
                        </div>
                    </div>

                    <button
                        type="button"
                        className="sidebar-mobile-close"
                        onClick={onMobileClose}
                        aria-label="بستن منو"
                    >
                        ×
                    </button>

                </div>

                <nav
                    className="tree-menu"
                    aria-label="منوی اصلی سامانه"
                >

                    {menu.map((group, index) => {

                        const isOpen = openMain === index;

                        return (
                            <div
                                key={index}
                                className="tree-group"
                            >

                                <button
                                    type="button"
                                    className="tree-title tree-main-title"
                                    onClick={() =>
                                        setOpenMain(
                                            isOpen ? null : index
                                        )
                                    }
                                    aria-expanded={isOpen}
                                >
                                    <span
                                        className="tree-toggle"
                                        aria-hidden="true"
                                    >
                                        {isOpen ? "−" : "+"}
                                    </span>

                                    <span className="tree-text">
                                        {group.title}
                                    </span>
                                </button>

                                {isOpen && (
                                    <div className="tree-children tree-main-children">
                                        {renderSubmenu(group.items)}
                                    </div>
                                )}

                            </div>
                        );
                    })}

                    <div className="tree-group">

                        <button
                            type="button"
                            className="tree-title tree-main-title"
                            onClick={() =>
                                setOpenMain(
                                    openMain === 99 ? null : 99
                                )
                            }
                            aria-expanded={openMain === 99}
                        >
                            <span className="tree-toggle">
                                {openMain === 99 ? "−" : "+"}
                            </span>

                            <span className="tree-text">
                                ادارات شهرستان
                            </span>
                        </button>

                        {openMain === 99 && (
                            <div className="tree-children tree-main-children">

                                {countyList.map((county) => {

                                    const isOpen =
                                        openCounty === county.path;

                                    return (
                                        <div
                                            key={county.path}
                                            className="tree-node"
                                        >

                                            <button
                                                type="button"
                                                className="tree-title tree-title-nested county-menu"
                                                onClick={() =>
                                                    setOpenCounty(
                                                        isOpen
                                                            ? null
                                                            : county.path
                                                    )
                                                }
                                                aria-expanded={isOpen}
                                            >
                                                <span className="tree-toggle">
                                                    {isOpen ? "−" : "+"}
                                                </span>

                                                <span className="tree-text">
                                                    {county.title}
                                                </span>
                                            </button>

                                            {isOpen && (
                                                <div className="tree-children">

                                                    <button
                                                        type="button"
                                                        className="tree-child"
                                                        onClick={() =>
                                                            handleNavigate(
                                                                county.path
                                                            )
                                                        }
                                                    >
                                                        داشبورد مدیریتی شهرستان
                                                    </button>

                                                    <button
                                                        type="button"
                                                        className="tree-child"
                                                        onClick={() =>
                                                            handleNavigate(
                                                                county.path +
                                                                "/expert/supervision"
                                                            )
                                                        }
                                                    >
                                                        کارشناس نظارت و بازرسی
                                                    </button>

                                                    <button
                                                        type="button"
                                                        className="tree-child"
                                                        onClick={() =>
                                                            handleNavigate(
                                                                county.path +
                                                                "/expert/disease"
                                                            )
                                                        }
                                                    >
                                                        کارشناس مدیریت بیماری‌ها
                                                    </button>

                                                </div>
                                            )}

                                        </div>
                                    );
                                })}

                            </div>
                        )}

                    </div>

                </nav>
            </aside>
        </>
    );
}

