import { createTheme } from '@mui/material'
import { components } from './components'
import { typography } from './typography'
import { getPalette } from './palette'

export const themeConstants = {
  navbarSize: 60,
  navbarAdd: 150,
  scrollWidth: 35
}

//sets the color mode on the palette object and conditionally chooses the palette
export const theme = createTheme({
  colorSchemes: {
    light: getPalette('light'),
    dark: getPalette('dark')
  },
  components: components,
  typography: typography
})
