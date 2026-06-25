import type { AppState, EmbedsValidationStatus } from "@excalidraw/excalidraw/types";
import type { ElementShape, ElementShapes } from "@excalidraw/excalidraw/scene/types";
import type { ExcalidrawElement } from "./types";
import type { Drawable } from "roughjs/bin/core";
export declare class ShapeCache {
    private static rg;
    private static cache;
    /**
     * Retrieves shape from cache if available. Use this only if shape
     * is optional and you have a fallback in case it's not cached.
     */
    static get: <T extends ExcalidrawElement>(element: T) => T["type"] extends keyof ElementShapes ? ElementShapes[T["type"]] | undefined : ElementShape | undefined;
    static set: <T extends ExcalidrawElement>(element: T, shape: T["type"] extends keyof ElementShapes ? ElementShapes[T["type"]] : Drawable) => WeakMap<ExcalidrawElement, ElementShape>;
    static delete: (element: ExcalidrawElement) => boolean;
    static destroy: () => void;
    /**
     * Generates & caches shape for element if not already cached, otherwise
     * returns cached shape.
     */
    static generateElementShape: <T extends import("./types").ExcalidrawLinearElement | import("./types").ExcalidrawRectangleElement | import("./types").ExcalidrawDiamondElement | import("./types").ExcalidrawEllipseElement | import("./types").ExcalidrawEmbeddableElement | import("./types").ExcalidrawIframeElement | import("./types").ExcalidrawImageElement | import("./types").ExcalidrawFrameElement | import("./types").ExcalidrawMagicFrameElement | import("./types").ExcalidrawTextElement | import("./types").ExcalidrawFreeDrawElement | import("./types").ExcalidrawArrowElement>(element: T, renderConfig: {
        isExporting: boolean;
        canvasBackgroundColor: AppState["viewBackgroundColor"];
        embedsValidationStatus: EmbedsValidationStatus;
    } | null) => ((T["type"] extends keyof ElementShapes ? ElementShapes[T["type"]] | undefined : ElementShape | undefined) & ({} | null)) | (T["type"] extends keyof ElementShapes ? ElementShapes[T["type"]] : Drawable | null);
}
