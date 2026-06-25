import React from "react";
import "./PasteChartDialog.scss";
import type { UIAppState } from "../types";
export declare const PasteChartDialog: ({ setAppState, appState, onClose, }: {
    appState: UIAppState;
    onClose: () => void;
    setAppState: React.Component<any, UIAppState>["setState"];
}) => import("react/jsx-runtime").JSX.Element;
