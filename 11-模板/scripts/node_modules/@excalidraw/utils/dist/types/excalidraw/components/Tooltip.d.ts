import React from "react";
import "./Tooltip.scss";
export declare const getTooltipDiv: () => HTMLDivElement;
export declare const updateTooltipPosition: (tooltip: HTMLDivElement, item: {
    left: number;
    top: number;
    width: number;
    height: number;
}, position?: "bottom" | "top") => void;
type TooltipProps = {
    children: React.ReactNode;
    label: string;
    long?: boolean;
    style?: React.CSSProperties;
    disabled?: boolean;
};
export declare const Tooltip: ({ children, label, long, style, disabled, }: TooltipProps) => import("react/jsx-runtime").JSX.Element | null;
export {};
