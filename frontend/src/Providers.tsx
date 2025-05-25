import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { App } from './App'
import { StockMockThemeProvider } from './theme'

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
