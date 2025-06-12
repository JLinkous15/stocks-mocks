import { CssBaseline, StyledEngineProvider, ThemeProvider, ThemeProvider as ThemeProviderProps } from "@mui/material"
import { theme } from "../theme/theme"

interface ThemeProviderProps {
  children: React.ReactNode
}

export const StockMockThemeProvider = ({ children }: ThemeProviderProps) => {
  return (
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </StyledEngineProvider>
  )
}
