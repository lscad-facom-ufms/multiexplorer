import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    sourcemap: true,
  },
  test: {
    globals: true,
  },
  plugins: [react()],
})
