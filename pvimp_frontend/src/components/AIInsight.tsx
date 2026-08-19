import React from "react";

type AIInsightProps = {
    title?: string;
    message?: string;
};

export default function AIInsight({
    title = "بینش هوشمند",
    message = "تحلیل و پیشنهاد هوشمند بر اساس داده‌های سامانه در این بخش نمایش داده می‌شود."
}: AIInsightProps) {
    return (
        <section
            className="pv-ai-insight"
            dir="rtl"
            aria-label={title}
        >
            <h3>{title}</h3>
            <p>{message}</p>
        </section>
    );
}