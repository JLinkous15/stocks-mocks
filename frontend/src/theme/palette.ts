import { createColorScheme } from "@mui/material";
import { SupportedColorScheme } from "@mui/material/styles"

export const lightPalette = createColorScheme({})

export const darkPalette = createColorScheme({})

export const getPalette = (theme: SupportedColorScheme) => {
    if (theme === 'light') return lightPalette

    return darkPalette
}
