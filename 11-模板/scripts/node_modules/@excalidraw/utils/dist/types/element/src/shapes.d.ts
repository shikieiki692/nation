import { type GlobalPoint, type LocalPoint } from "@excalidraw/math";
import { type GeometricShape } from "@excalidraw/utils/shape";
import type { Zoom } from "@excalidraw/excalidraw/types";
import { type Bounds } from "./bounds";
import type { ElementsMap, ExcalidrawElement, ExcalidrawLinearElement, NonDeleted } from "./types";
/**
 * get the pure geometric shape of an excalidraw elementw
 * which is then used for hit detection
 */
export declare const getElementShape: <Point extends GlobalPoint | LocalPoint>(element: ExcalidrawElement, elementsMap: ElementsMap) => GeometricShape<Point>;
export declare const getBoundTextShape: <Point extends GlobalPoint | LocalPoint>(element: ExcalidrawElement, elementsMap: ElementsMap) => GeometricShape<Point> | null;
export declare const getControlPointsForBezierCurve: <P extends GlobalPoint | LocalPoint>(element: NonDeleted<ExcalidrawLinearElement>, endPoint: P) => P[] | null;
export declare const getBezierXY: <P extends GlobalPoint | LocalPoint>(p0: P, p1: P, p2: P, p3: P, t: number) => P;
export declare const getBezierCurveLength: <P extends GlobalPoint | LocalPoint>(element: NonDeleted<ExcalidrawLinearElement>, endPoint: P) => number;
export declare const mapIntervalToBezierT: <P extends GlobalPoint | LocalPoint>(element: NonDeleted<ExcalidrawLinearElement>, endPoint: P, interval: number) => number;
/**
 * Get the axis-aligned bounding box for a given element
 */
export declare const aabbForElement: (element: Readonly<ExcalidrawElement>, offset?: [number, number, number, number]) => Bounds;
export declare const pointInsideBounds: <P extends GlobalPoint | LocalPoint>(p: P, bounds: Bounds) => boolean;
export declare const aabbsOverlapping: (a: Bounds, b: Bounds) => boolean;
export declare const getCornerRadius: (x: number, element: ExcalidrawElement) => number;
export declare const isPathALoop: (points: ExcalidrawLinearElement["points"], zoomValue?: Zoom["value"]) => boolean;
