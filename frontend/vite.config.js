import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/link': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/exchange': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/sync': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/webhook': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/transactions': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/tips': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/sandbox': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
