import type { ColorPaletteCustom } from "@excalidraw/common";
interface ShadeListProps {
    hex: string;
    onChange: (color: string) => void;
    palette: ColorPaletteCustom;
}
export declare const ShadeList: ({ hex, onChange, palette }: ShadeListProps) => import("react/jsx-runtime").JSX.Element;
export {};
