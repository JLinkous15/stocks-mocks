import { LOCAL_STORAGE_KEY, useDarkMode } from "../hooks/useDarkMode"
import { Stack, SupportedColorScheme, Switch } from "@mui/material"
import LightModeIcon from '@mui/icons-material/LightMode'
import DarkModeIcon from '@mui/icons-material/ModeNight'

const size = 'small'

export const ColorModeSwitch = () => {
    const {mode, setMode} = useDarkMode()

    const handleSwitch = (_: React.ChangeEvent<HTMLInputElement>, checked: boolean) => {
        const nextMode: SupportedColorScheme = checked ? 'dark' : 'light'

        setMode(nextMode)
        localStorage.setItem(LOCAL_STORAGE_KEY, nextMode)
    }

    return (
        <Stack direction="row" alignItems="center" padding={2}>
            <LightModeIcon color="primary" fontSize={size} />
            <Switch checked={mode==='dark'} onChange={handleSwitch} />
            <DarkModeIcon color="primary" fontSize={size} />
        </Stack>
    )
}