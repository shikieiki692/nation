import { type GlobalPoint, type LocalPoint, type Polygon } from "@excalidraw/math";
import type { Curve } from "@excalidraw/math";
import type { Polyline, GeometricShape } from "./shape";
export declare const isPointOnShape: <Point extends GlobalPoint | LocalPoint>(point: Point, shape: GeometricShape<Point>, tolerance?: number) => boolean;
export declare const isPointInShape: <Point extends GlobalPoint | LocalPoint>(point: Point, shape: GeometricShape<Point>) => boolean;
export declare const isPointInBounds: <Point extends GlobalPoint | LocalPoint>(point: Point, bounds: Polygon<Point>) => boolean;
export declare const pointOnCurve: <Point extends GlobalPoint | LocalPoint>(point: Point, curve: Curve<Point>, threshold: number) => boolean;
export declare const pointOnPolyline: <Point extends GlobalPoint | LocalPoint>(point: Point, polyline: Polyline<Point>, threshold?: number) => boolean;
