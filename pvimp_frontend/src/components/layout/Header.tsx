import React from "react";
import "./Header.css";

export default function Header() {
    return (
        <header className="app-header" dir="rtl">

            <div className="app-header__right">

                <div className="app-header__icon">
                    دام
                </div>

                <div className="app-header__titles">
                    <h1>
                        سامانه مدیریت یکپارچه دامپزشکی
                    </h1>

                    <span>
                        اداره کل دامپزشکی استان زنجان
                    </span>
                </div>

            </div>

            <div className="app-header__left">

                <div className="app-header__status">
                    <span className="app-header__status-dot" />
                    سامانه فعال
                </div>

                <div className="app-header__user">
                    <div className="app-header__avatar">
                        ک
                    </div>

                    <div className="app-header__user-info">
                        <strong>
                            کاربر سامانه
                        </strong>

                        <span>
                            مدیریت استان
                        </span>
                    </div>
                </div>

            </div>

        </header>
    );
}
