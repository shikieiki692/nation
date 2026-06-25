import type { OrderedExcalidrawElement } from "@excalidraw/element/types";
import type { MakeBrand } from "@excalidraw/common/utility-types";
import type { AppState } from "../types";
export type ReconciledExcalidrawElement = OrderedExcalidrawElement & MakeBrand<"ReconciledElement">;
export type RemoteExcalidrawElement = OrderedExcalidrawElement & MakeBrand<"RemoteExcalidrawElement">;
export declare const reconcileElements: (localElements: readonly OrderedExcalidrawElement[], remoteElements: readonly RemoteExcalidrawElement[], localAppState: AppState) => ReconciledExcalidrawElement[];
