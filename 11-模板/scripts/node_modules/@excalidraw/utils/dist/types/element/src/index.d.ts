import type { ExcalidrawElement, NonDeletedExcalidrawElement, NonDeleted } from "./types";
/**
 * @deprecated unsafe, use hashElementsVersion instead
 */
export declare const getSceneVersion: (elements: readonly ExcalidrawElement[]) => number;
/**
 * Hashes elements' versionNonce (using djb2 algo). Order of elements matters.
 */
export declare const hashElementsVersion: (elements: readonly ExcalidrawElement[]) => number;
export declare const hashString: (s: string) => number;
export declare const getVisibleElements: (elements: readonly ExcalidrawElement[]) => readonly NonDeletedExcalidrawElement[];
export declare const getNonDeletedElements: <T extends ExcalidrawElement>(elements: readonly T[]) => readonly NonDeleted<T>[];
export declare const isNonDeletedElement: <T extends ExcalidrawElement>(element: T) => element is NonDeleted<T>;
export declare const clearElementsForDatabase: (elements: readonly ExcalidrawElement[]) => ExcalidrawElement[];
export declare const clearElementsForExport: (elements: readonly ExcalidrawElement[]) => ExcalidrawElement[];
export declare const clearElementsForLocalStorage: (elements: readonly ExcalidrawElement[]) => ExcalidrawElement[];
