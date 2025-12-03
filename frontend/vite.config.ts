import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0'
  },
  define: {
    __API_BASE__: JSON.stringify(process.env.VITE_API_BASE || 'http://localhost:8000/api/v1')
  }
});
