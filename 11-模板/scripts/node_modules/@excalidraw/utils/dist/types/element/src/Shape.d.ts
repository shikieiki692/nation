import type { EmbedsValidationStatus } from "@excalidraw/excalidraw/types";
import type { ExcalidrawElement, NonDeletedExcalidrawElement, ExcalidrawSelectionElement } from "./types";
import type { Drawable, Options } from "roughjs/bin/core";
import type { RoughGenerator } from "roughjs/bin/generator";
export declare const generateRoughOptions: (element: ExcalidrawElement, continuousPath?: boolean) => Options;
/**
 * Generates the roughjs shape for given element.
 *
 * Low-level. Use `ShapeCache.generateElementShape` instead.
 *
 * @private
 */
export declare const _generateElementShape: (element: Exclude<NonDeletedExcalidrawElement, ExcalidrawSelectionElement>, generator: RoughGenerator, { isExporting, canvasBackgroundColor, embedsValidationStatus, }: {
    isExporting: boolean;
    canvasBackgroundColor: string;
    embedsValidationStatus: EmbedsValidationStatus | null;
}) => Drawable | Drawable[] | null;
