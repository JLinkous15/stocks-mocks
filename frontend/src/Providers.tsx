import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { App } from './App'
import { StockMockThemeProvider } from './components/StockMarketThemeProvider'

const queryClient = new QueryClient()

export const Providers = () => {

  return (
    <QueryClientProvider client={queryClient}>
      <StockMockThemeProvider>
        <App />
      </StockMockThemeProvider>
    </QueryClientProvider>
  )
}
