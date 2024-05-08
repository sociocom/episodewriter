import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  base: '/episodewriter/',
  server: {
    host: true,
    port: 80,
    watch: {
      usePolling: true,
    },
    proxy: {
      "/episodewriter/api": {
        target: "http://backend:8888",
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/episodewriter/, ''),
      },
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
