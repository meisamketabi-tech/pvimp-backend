import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { login, getCurrentUser } from "../services/auth.service";
import { useAuthStore } from "../store/auth.store";
import { getToken, removeToken } from "../utils/token";
import logo from "../assets/vet-logo.svg";
import "./Login.css";

export default function LoginV2() {
    const navigate = useNavigate();
    const location = useLocation();
    const authLogin = useAuthStore((state) => state.login);
    const setUser = useAuthStore((state) => state.setUser);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [checkingSession, setCheckingSession] = useState(true);
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        let active = true;
        async function checkSession() {
            const token = getToken();
            if (!token) {
                if (active) setCheckingSession(false);
                return;
            }
            try {
                const currentUser = await getCurrentUser();
                if (!active) return;
                setUser(currentUser);
                navigate("/", { replace: true });
            } catch {
                removeToken();
                if (active) setCheckingSession(false);
            }
        }
        void checkSession();
        return () => { active = false; };
    }, [navigate, setUser]);

    async function submit(e: React.FormEvent) {
        e.preventDefault();
        setError("");
        setSubmitting(true);
        try {
            const result = await login({ username: username.trim(), password });
            authLogin(result.access_token);
            const currentUser = await getCurrentUser();
            setUser(currentUser);
            const from = (location.state as { from?: string } | null)?.from;
            navigate(from || "/", { replace: true });
        } catch (error: any) {
            console.error("LOGIN ERROR", error);
            setError(error.response?.data?.detail || "نام کاربری یا رمز عبور صحیح نیست.");
        } finally {
            setSubmitting(false);
        }
    }

    if (checkingSession) {
        return (
            <div className="login-page" dir="rtl">
                <div className="login-session-check">
                    <img src={logo} alt="دامپزشکی" />
                    <strong>در حال بررسی وضعیت ورود...</strong>
                </div>
            </div>
        );
    }

    return (
        <div className="login-page" dir="rtl">
            <div className="login-background-orb login-background-orb--one" />
            <div className="login-background-orb login-background-orb--two" />
            <div className="login-container">
                <section className="login-brand">
                    <div className="login-logo-wrap"><img src={logo} className="login-logo" alt="نشان دامپزشکی" /></div>
                    <span className="login-eyebrow">VET • SMART MANAGEMENT</span>
                    <h1>سامانه مدیریت یکپارچه دامپزشکی</h1>
                    <p>سیستم هوشمند مدیریت، پایش و نظارت دامپزشکی استان زنجان</p>
                    <div className="login-brand-line" />
                    <small>اداره کل دامپزشکی استان زنجان</small>
                </section>
                <section className="login-form-panel">
                    <div className="login-form-heading">
                        <span>ورود امن</span>
                        <h2>ورود به سامانه</h2>
                        <p>برای ادامه، نام کاربری و رمز عبور خود را وارد کنید.</p>
                    </div>
                    <form onSubmit={submit} className="login-form">
                        <label className="login-field">
                            <span>نام کاربری</span>
                            <input autoFocus autoComplete="username" className="login-input" placeholder="نام کاربری خود را وارد کنید" value={username} onChange={(e) => setUsername(e.target.value)} required />
                        </label>
                        <label className="login-field">
                            <span>رمز عبور</span>
                            <input type="password" autoComplete="current-password" className="login-input" placeholder="رمز عبور خود را وارد کنید" value={password} onChange={(e) => setPassword(e.target.value)} required />
                        </label>
                        {error && <div className="login-error">{error}</div>}
                        <button className="login-button" type="submit" disabled={submitting}>{submitting ? "در حال ورود..." : "ورود به سامانه"}</button>
                    </form>
                    <div className="login-security-note"><span className="login-security-dot" /> نشست شما پس از ورود به‌صورت امن بررسی می‌شود.</div>
                </section>
            </div>
        </div>
    );
}
