import type { AppClassProperties } from "../types";
export declare const actionTextAutoResize: {
    name: "autoResize";
    label: string;
    icon: null;
    trackEvent: {
        category: "element";
    };
    predicate: (elements: readonly import("../../element/src/types").ExcalidrawElement[], appState: import("../types").AppState, _: unknown, app: AppClassProperties) => boolean;
    perform: (elements: readonly import("../../element/src/types").OrderedExcalidrawElement[], appState: Readonly<import("../types").AppState>, _: any, app: AppClassProperties) => {
        appState: Readonly<import("../types").AppState>;
        elements: import("../../element/src/types").OrderedExcalidrawElement[];
        captureUpdate: "IMMEDIATELY";
    };
} & {
    keyTest?: undefined;
};
