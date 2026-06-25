import "./HintViewer.scss";
import type { AppClassProperties, Device, UIAppState } from "../types";
interface HintViewerProps {
    appState: UIAppState;
    isMobile: boolean;
    device: Device;
    app: AppClassProperties;
}
export declare const HintViewer: ({ appState, isMobile, device, app, }: HintViewerProps) => import("react/jsx-runtime").JSX.Element | null;
export {};
