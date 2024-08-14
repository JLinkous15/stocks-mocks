import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query'
import { StockMockThemeProvider } from './theme'
import { App } from './App'

const queryClient = new QueryClient()

export function Providers() {
  // const {isLoading, data, isError} = useQuery({
  //   queryFn: () => {},
  //   queryKey: ["query"],

  // })

  return (
    <QueryClientProvider client={queryClient}>
      <StockMockThemeProvider>
        <App />
      </StockMockThemeProvider>
    </QueryClientProvider>
  )
}
