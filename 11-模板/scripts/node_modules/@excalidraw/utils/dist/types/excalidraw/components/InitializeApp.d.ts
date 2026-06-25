import React from "react";
import type { Theme } from "@excalidraw/element/types";
import type { Language } from "../i18n";
interface Props {
    langCode: Language["code"];
    children: React.ReactElement;
    theme?: Theme;
}
export declare const InitializeApp: (props: Props) => import("react/jsx-runtime").JSX.Element;
export {};
