import React, { useEffect } from "react";
import "./Modal.css";

type ModalSize = "sm" | "md" | "lg" | "xl";

type ModalProps = {
    open: boolean;
    onClose: () => void;
    title?: string;
    children: React.ReactNode;
    size?: ModalSize;
    closeOnOverlay?: boolean;
    showClose?: boolean;
    footer?: React.ReactNode;
};

export default function Modal({
    open,
    onClose,
    title,
    children,
    size = "md",
    closeOnOverlay = true,
    showClose = true,
    footer
}: ModalProps) {
    useEffect(() => {
        if (!open) {
            return;
        }

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === "Escape") {
                onClose();
            }
        };

        document.addEventListener("keydown", handleKeyDown);

        return () => {
            document.removeEventListener("keydown", handleKeyDown);
        };
    }, [open, onClose]);

    useEffect(() => {
        if (!open) {
            return;
        }

        const previousOverflow = document.body.style.overflow;
        document.body.style.overflow = "hidden";

        return () => {
            document.body.style.overflow = previousOverflow;
        };
    }, [open]);

    if (!open) {
        return null;
    }

    const handleOverlayClick = (
        event: React.MouseEvent<HTMLDivElement>
    ) => {
        if (
            closeOnOverlay &&
            event.target === event.currentTarget
        ) {
            onClose();
        }
    };

    return (
        <div
            className="pv-modal-overlay"
            onMouseDown={handleOverlayClick}
            role="presentation"
        >
            <div
                className={`pv-modal pv-modal-${size}`}
                role="dialog"
                aria-modal="true"
                aria-labelledby={title ? "pv-modal-title" : undefined}
            >
                {(title || showClose) && (
                    <div className="pv-modal-header">
                        {title && (
                            <h2
                                id="pv-modal-title"
                                className="pv-modal-title"
                            >
                                {title}
                            </h2>
                        )}

                        {showClose && (
                            <button
                                type="button"
                                className="pv-modal-close"
                                onClick={onClose}
                                aria-label="بستن"
                            >
                                ×
                            </button>
                        )}
                    </div>
                )}

                <div className="pv-modal-body">
                    {children}
                </div>

                {footer && (
                    <div className="pv-modal-footer">
                        {footer}
                    </div>
                )}
            </div>
        </div>
    );
}