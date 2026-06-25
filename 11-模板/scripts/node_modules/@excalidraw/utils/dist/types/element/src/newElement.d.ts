import type { MarkOptional } from "@excalidraw/common/utility-types";
import type { ExcalidrawImageElement, ExcalidrawTextElement, ExcalidrawLinearElement, ExcalidrawGenericElement, NonDeleted, TextAlign, VerticalAlign, Arrowhead, ExcalidrawFreeDrawElement, FontFamilyValues, ExcalidrawTextContainer, ExcalidrawFrameElement, ExcalidrawEmbeddableElement, ExcalidrawMagicFrameElement, ExcalidrawIframeElement, ElementsMap, ExcalidrawArrowElement, FixedSegment, ExcalidrawElbowArrowElement } from "./types";
export type ElementConstructorOpts = MarkOptional<Omit<ExcalidrawGenericElement, "id" | "type" | "isDeleted" | "updated">, "width" | "height" | "angle" | "groupIds" | "frameId" | "index" | "boundElements" | "seed" | "version" | "versionNonce" | "link" | "strokeStyle" | "fillStyle" | "strokeColor" | "backgroundColor" | "roughness" | "strokeWidth" | "roundness" | "locked" | "opacity" | "customData">;
export declare const newElement: (opts: {
    type: ExcalidrawGenericElement["type"];
} & ElementConstructorOpts) => NonDeleted<ExcalidrawGenericElement>;
export declare const newEmbeddableElement: (opts: {
    type: "embeddable";
} & ElementConstructorOpts) => NonDeleted<ExcalidrawEmbeddableElement>;
export declare const newIframeElement: (opts: {
    type: "iframe";
} & ElementConstructorOpts) => NonDeleted<ExcalidrawIframeElement>;
export declare const newFrameElement: (opts: {
    name?: string;
} & ElementConstructorOpts) => NonDeleted<ExcalidrawFrameElement>;
export declare const newMagicFrameElement: (opts: {
    name?: string;
} & ElementConstructorOpts) => NonDeleted<ExcalidrawMagicFrameElement>;
export declare const newTextElement: (opts: {
    text: string;
    originalText?: string;
    fontSize?: number;
    fontFamily?: FontFamilyValues;
    textAlign?: TextAlign;
    verticalAlign?: VerticalAlign;
    containerId?: ExcalidrawTextContainer["id"] | null;
    lineHeight?: ExcalidrawTextElement["lineHeight"];
    autoResize?: ExcalidrawTextElement["autoResize"];
} & ElementConstructorOpts) => NonDeleted<ExcalidrawTextElement>;
export declare const refreshTextDimensions: (textElement: ExcalidrawTextElement, container: ExcalidrawTextContainer | null, elementsMap: ElementsMap, text?: string) => {
    x: number;
    y: number;
    width: number;
    height: number;
    text: string;
} | undefined;
export declare const newFreeDrawElement: (opts: {
    type: "freedraw";
    points?: ExcalidrawFreeDrawElement["points"];
    simulatePressure: boolean;
    pressures?: ExcalidrawFreeDrawElement["pressures"];
} & ElementConstructorOpts) => NonDeleted<ExcalidrawFreeDrawElement>;
export declare const newLinearElement: (opts: {
    type: ExcalidrawLinearElement["type"];
    points?: ExcalidrawLinearElement["points"];
} & ElementConstructorOpts) => NonDeleted<ExcalidrawLinearElement>;
export declare const newArrowElement: <T extends boolean>(opts: {
    type: ExcalidrawArrowElement["type"];
    startArrowhead?: Arrowhead | null | undefined;
    endArrowhead?: Arrowhead | null | undefined;
    points?: readonly import("@excalidraw/math").LocalPoint[] | undefined;
    elbowed?: T | undefined;
    fixedSegments?: FixedSegment[] | null | undefined;
} & Omit<Omit<ExcalidrawGenericElement, "id" | "isDeleted" | "updated" | "type">, "link" | "strokeColor" | "backgroundColor" | "fillStyle" | "strokeWidth" | "strokeStyle" | "roundness" | "roughness" | "opacity" | "width" | "height" | "angle" | "seed" | "version" | "versionNonce" | "index" | "groupIds" | "frameId" | "boundElements" | "locked" | "customData"> & Partial<Pick<Omit<ExcalidrawGenericElement, "id" | "isDeleted" | "updated" | "type">, "link" | "strokeColor" | "backgroundColor" | "fillStyle" | "strokeWidth" | "strokeStyle" | "roundness" | "roughness" | "opacity" | "width" | "height" | "angle" | "seed" | "version" | "versionNonce" | "index" | "groupIds" | "frameId" | "boundElements" | "locked" | "customData">>) => T extends true ? NonDeleted<ExcalidrawElbowArrowElement> : NonDeleted<ExcalidrawArrowElement>;
export declare const newImageElement: (opts: {
    type: ExcalidrawImageElement["type"];
    status?: ExcalidrawImageElement["status"];
    fileId?: ExcalidrawImageElement["fileId"];
    scale?: ExcalidrawImageElement["scale"];
    crop?: ExcalidrawImageElement["crop"];
} & ElementConstructorOpts) => NonDeleted<ExcalidrawImageElement>;
