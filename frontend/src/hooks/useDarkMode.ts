import { SupportedColorScheme, useColorScheme, useMediaQuery } from "@mui/material"
import { useEffect } from "react"

export const LOCAL_STORAGE_KEY = 'stock-mock-color-mode'

export const useDarkMode = () => {
    const {mode, setMode} = useColorScheme()
    const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)')

    const setColorMode = (mode: SupportedColorScheme) => {
        localStorage.setItem(LOCAL_STORAGE_KEY, mode)
        setMode(mode)
    }

    useEffect(() => {
        const storedMode = localStorage.getItem(LOCAL_STORAGE_KEY)

        if (storedMode) {
            setMode(storedMode as 'dark' | 'light')
        } else if (prefersDarkMode) {
            setColorMode('dark')
        } else {
            setColorMode('light')
        }
    }, [])

    return {mode, setMode}
}