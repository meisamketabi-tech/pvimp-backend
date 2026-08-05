import React from "react";
import UIShowcase from "../components/ui/UIShowcase";

export default function UIComponents() {

    return (
        <main
            style={{
                width: "100%",
                minHeight: "100%",
                padding: "24px",
                boxSizing: "border-box",
                direction: "rtl"
            }}
        >
            <UIShowcase />
        </main>
    );
}
